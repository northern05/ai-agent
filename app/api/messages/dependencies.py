from datetime import datetime
import hashlib

from app.llm import process_user_message
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import dependencies as auth_dependencies
from app.core.models import db_helper, User, Message
from . import crud
from .schemas import MessageSchema, DataIn, MessageResponse
from app.core.modules_factory import smc_driver


async def process_users_message(
        data_in: DataIn,
        user: User = Depends(auth_dependencies.check_wallet),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if not data_in.message or not data_in.transaction_hash:
        raise HTTPException(
            detail="No needed data received",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # verify msg hash from transaction and users hashed
    encoded_msg = hashlib.sha256(data_in.message.encode('utf-8')).hexdigest()
    encoded_msg_from_transaction = smc_driver.get_msg_hash(data_in.transaction_hash)
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
    # create messages in db
    user_msg = Message(
        user_id=user.id,
        role="user",
        content=data_in.message,
        tx_hash=data_in.transaction_hash,
        is_winner= True if llm_response.decision == "approve" else False,
        created_at=datetime.fromtimestamp(data_in.timestamp / 1000)
    )
    await crud.create(session=session, user_id=user.id, message=user_msg)

    system_msg = Message(
        user_id=user.id,
        role="system",
        content=llm_response.text,
        tx_hash=data_in.transaction_hash,
        is_winner=True if llm_response.decision == "approve" else False,
        created_at=datetime.now()
    )
    await crud.create(session=session, user_id=user.id, message=system_msg)

    timestamp = int(datetime.now().timestamp() * 1000)
    result = MessageResponse(
        body=llm_response.text,
        decision=llm_response.decision,
        timestamp=timestamp
    )

    return result
