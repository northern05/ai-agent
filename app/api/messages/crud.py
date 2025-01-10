from datetime import datetime

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_sa_orm_filter.main import FilterCore
from fastapi_sa_orm_filter.operators import Operators as ops

from app.core.models import Message
from utils.paginated_response import paginate, PaginatedParams, PaginatedResponse
from .schemas import MessageSchema

message_query_filters = {
    'created_at': [ops.gte, ops.lte, ops.eq],
    'user_id': [ops.eq]
}


async def get_all(
        session: AsyncSession,
        pagination_query: PaginatedParams,
        filter_query: str
) -> PaginatedResponse[MessageSchema]:
    filter_inst = MessageFilter(Message, message_query_filters)
    stmt = filter_inst.get_query(filter_query)
    response, data = await paginate(
        session=session, query=stmt,
        page_size=pagination_query.page_size, page_number=pagination_query.page_number
    )

    res = []
    for c in data:
        r = MessageSchema.model_validate(c)
        res.append(r)
    response["data"] = res

    return response


class MessageFilter(FilterCore):

    def get_select_query_part(self):
        return (
            select(Message).order_by(Message.created_at.desc())
        )


async def create(session: AsyncSession, user_id: int, message: Message) -> Message | None:
    message = Message(
        created_at=datetime.now(),
        user_id=user_id,
        content=message.content,
        response=message.response,
        decision=message.decision
    )
    session.add(message)
    await session.commit()
    return message


async def select_by_id(session: AsyncSession, chat_id: int) -> Message | None:
    stmt = (
        select(Message)
        .filter(Message.id == chat_id)
    )
    result: Result = await session.execute(stmt)
    msg = result.scalars().first()
    return msg