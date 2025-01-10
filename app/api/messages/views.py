import logging

from fastapi.params import Query
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import dependencies as auth_dependencies
from app.core.models import db_helper, Chat, User
from utils.paginated_response import PaginatedResponse, PaginatedParams
from . import crud
from . import dependencies
from .schemas import MessageSchema

router = APIRouter(tags=["Chats"])

logger = logging.getLogger('chats/views')


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[MessageSchema],
)
async def get_all_chats(
        objects_filter: str = Query(default=''),
        pagination_query: PaginatedParams = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    logger.info("Received get all chats request")

    res = await crud.get_all(
        session=session,
        pagination_query=pagination_query,
        filter_query=objects_filter
    )
    return res


@router.post(
    "",
    status_code=status.HTTP_200_OK,
)
async def start_chat_streaming(
        response: MessageSchema = Depends(dependencies.process_users_message)
):
    return response
