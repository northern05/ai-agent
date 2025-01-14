import logging

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.statistics import crud
from app.core.models import db_helper

from app.api.statistics.schemas import MessageCountResponse, UsersCountResponse

router = APIRouter(tags=["Statistics"])

logger = logging.getLogger('statistics/views')


@router.get(
    "/messages",
    status_code=status.HTTP_200_OK,
    response_model=MessageCountResponse,
)
async def get_all_messages_count(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    logger.info("Received get messages count request")

    count = await crud.get_message_count(
        session=session,
    )
    return MessageCountResponse(total_messages=count)

@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=UsersCountResponse,
)
async def get_all_users_count(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    logger.info("Received get users count request")

    count = await crud.get_unique_users_count(
        session=session,
    )
    return UsersCountResponse(total_users=count)