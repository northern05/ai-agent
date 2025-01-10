import datetime
import json
from dataclasses import dataclass
from typing import Annotated
import jsonpickle

from app.core.models.user import User
from app.llm import process_user_message
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import dependencies as auth_dependencies
from app.core.errors import errors
from app.core.models import db_helper, Chat
from app.core.modules_factory import redis_db
from . import crud
from .schemas import ChatResponse, ExtendedChatSchema, DataIn


from app.core.config import superadmin_settings


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


@dataclass
class ChatContext:
    current_input: str
    current_dt: datetime.datetime
    history: list[dict]
    minimized_history: list[dict]
    chat_id: str


async def process_chat_request(
        data_in: DataIn,
        chat: ExtendedChatSchema = Depends(get_extended_chat_by_uuid),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ChatResponse:
    context = ChatContext(
        current_input=data_in.message,
        current_dt=datetime.datetime.now(),
        history=chat.history,
        minimized_history=_init_chatbot_history_context(chat),
        chat_id=chat.uuid
    )
    if not data_in.message:
        raise HTTPException(
            detail="No needed data received",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    _user_message = {
        "role": "user",
        "content": data_in.message,
        "parts": [data_in.message],
        "timestamp": data_in.timestamp
    }
    chat.history.append(_user_message)

    # llm_response = await process_user_message(
    #     message=data_in.message
    # )

    timestamp = int(datetime.datetime.now().timestamp() * 1000)
    res = ChatResponse(
        exec_logs="",
        body="mocked msg",
        decision="reject",
        timestamp=timestamp
    )

    chat.history.append({
        "role": "system",
        "content": "mocked msg",
        "parts": ["mocked msg"],
        "timestamp": timestamp,
        "decision": "reject"
    })

    redis_db.set(chat.uuid, jsonpickle.encode(chat.history))

    return res

async def process_test_msg(
        data_in: DataIn,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> ChatResponse:
    if not data_in.message:
        raise HTTPException(
            detail="No needed data received",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    _user_message = {
        "role": "user",
        "content": data_in.message,
        "parts": [data_in.message],
        "timestamp": data_in.timestamp
    }
    llm_response = await process_user_message(
        message=data_in.message
    )

    timestamp = int(datetime.datetime.now().timestamp() * 1000)
    res = ChatResponse(
        exec_logs="",
        body=llm_response.text,
        decision=llm_response.decision,
        timestamp=timestamp
    )

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


async def chat_to_redis():
    ...


async def chat_from_redis():
    ...


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
