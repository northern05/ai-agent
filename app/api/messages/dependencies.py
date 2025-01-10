import datetime
import hashlib

from app.llm import process_user_message
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import dependencies as auth_dependencies
from app.core.models import db_helper, User
from . import crud
from .schemas import MessageSchema, DataIn, MessageResponse
from app.core.modules_factory import smc_driver


async def process_users_message(
        data_in: DataIn,
        user: User = Depends(auth_dependencies.extract_user_from_access_token),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if not data_in.message or not data_in.transaction_hash:
        raise HTTPException(
            detail="No needed data received",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    encoded_msg = hashlib.sha256(data_in.message.encode('utf-8')).hexdigest()
    encoded_msg_from_transaction = smc_driver.get_msg_hash(data_in.transaction_hash)
    if encoded_msg != encoded_msg_from_transaction:
        raise HTTPException(
            detail="Messages doesn't match!",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    llm_response = await process_user_message(
        message=data_in.message
    )
    msg = MessageSchema(
        user_id=user.id,
        decision=llm_response.decision,
        response=llm_response.text,
        content=data_in.message
    )
    await crud.create(session=session, user_id=user.id, message=msg)

    timestamp = int(datetime.datetime.now().timestamp() * 1000)
    result = MessageResponse(
        exec_logs="",
        body=llm_response.text,
        decision=llm_response.decision,
        timestamp=timestamp
    )

    return result
