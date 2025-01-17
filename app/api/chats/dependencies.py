import datetime
import hashlib
import json

from typing import Annotated
import jsonpickle

from app.core.models.user import User
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import dependencies as auth_dependencies
from app.core.errors import errors
from app.core.models import db_helper, Chat
from app.core.modules_factory import redis_db, smc_driver
from . import crud
from .schemas import ChatResponse, ExtendedChatSchema, DataIn


from app.core.config import superadmin_settings
from ...core.models.base import State
from ...core.models.message import Role
from ...llm import process_user_message


async def get_chat_by_id(
        chat_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Chat:
    chat = await crud.select_by_id(session=session, chat_id=chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=errors.chats.CHAT_NOT_FOUND
        )

    return chat


async def get_chat_by_uuid(
        chat_uuid: Annotated[str, Path],
        user: User = Depends(auth_dependencies.extract_user_from_access_token),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Chat:
    chat = await crud.select_by_uuid(session=session, chat_uuid=chat_uuid)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=errors.chats.CHAT_NOT_FOUND
        )

    if user.wallet != superadmin_settings.SUPERADMIN_WALLET_ADDRESS and chat.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=errors.chats.USER_NOT_OWNER
        )

    return chat


async def get_extended_chat_by_uuid(
        chat_uuid: Annotated[str, Path],
        user=Depends(auth_dependencies.extract_user_from_access_token),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ExtendedChatSchema:
    chat = await get_chat_by_uuid(chat_uuid, user, session)

    chat = ExtendedChatSchema.from_orm(chat)
    history = redis_db.get(chat.uuid)
    if history:
        chat.history = json.loads(history)
    else:
        chat.history = []

    return chat

async def process_chat_request(
        data_in: DataIn,
        chat: ExtendedChatSchema = Depends(get_extended_chat_by_uuid),
        user: User = Depends(auth_dependencies.check_wallet),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ChatResponse:
    if chat.state == State.deleted:
        raise HTTPException(
            detail="Chat is already deleted",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not data_in.message or not data_in.msg_hash:
        raise HTTPException(
            detail="No needed data received",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # verify msg hash from transaction and users hashed
    encoded_msg = hashlib.sha256(data_in.message.encode('utf-8')).hexdigest()
    encoded_msg_from_transaction = smc_driver.get_swap_msg_hash(data_in.transaction_hash)
    if encoded_msg != encoded_msg_from_transaction:
        raise HTTPException(
            detail="Messages doesn't match!",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # processing user's message
    llm_response = await process_user_message(
        message=data_in.message,
        smc_driver=smc_driver,
        user_address=user.wallet
    )

    _user_message = {
        "role": Role.user,
        "content": data_in.message,
        "tx_hash": data_in.transaction_hash,
        "parts": [data_in.message],
        "timestamp": data_in.timestamp,
        "is_approved": True if llm_response.decision == "approveSwap" else False,
    }
    chat.history.append(_user_message)

    timestamp = int(datetime.datetime.now().timestamp() * 1000)
    res = ChatResponse(
        exec_logs="",
        body=llm_response.text,
        decision=llm_response.decision,
        timestamp=timestamp
    )

    chat.history.append({
        "role": Role.system,
        "content": llm_response.text,
        "parts": [llm_response.text],
        "timestamp": timestamp,
        "is_approved": True if llm_response.decision == "approveSwap" else False,
        "decision": llm_response.decision
    })

    redis_db.set(chat.uuid, jsonpickle.encode(chat.history))

    return res

request_actions = {
    "askUserAddress()": "askUserAddress()",
    "askTransactionAmount()": "askTransactionAmount()",
}


def _init_chatbot_history_context(chat):
    """Minimizes redis-stored history for bot requests."""
    chat_history_context = []
    for message_dict in chat.history:
        chat_history_context.append({"role": message_dict["role"], "content": message_dict["content"]})
    return chat_history_context

async def start_new_chat(
        user=Depends(auth_dependencies.extract_user_from_access_token),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    chat = await crud.create(session=session, user_id=user.id)
    redis_db.set(chat.uuid, json.dumps([]))

    return chat


def _process_generated_output(text: str):
    t_blocks = text.split("{-==-}")
    if len(t_blocks) == 1:
        return text, []
    if len(t_blocks) > 1:
        output = t_blocks[0]
        contains_strategy_previews = t_blocks[1].split(",")
        contains_strategy_previews = [x.strip() for x in contains_strategy_previews]

        return output, contains_strategy_previews
