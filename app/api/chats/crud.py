import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Chat
from utils.paginated_response import paginate, PaginatedParams, PaginatedResponse
from .schemas import ChatSchema
from .schemas import ChatUpdate, ChatUpdatePartial
from ...core.models.base import State


async def get_all(
        session: AsyncSession,
        pagination_query: PaginatedParams,
        user_id: int = None
) -> PaginatedResponse[ChatSchema]:
    stmt = (
        select(Chat)
        .filter(Chat.state != State.deleted)
        .filter(not user_id or Chat.user_id == user_id)
        .order_by(Chat.created_at.desc())
    )
    response, data = await paginate(
        session=session, query=stmt,
        page_size=pagination_query.page_size, page_number=pagination_query.page_number
    )

    res = []
    for c in data:
        r = ChatSchema.model_validate(c)
        res.append(r)
    response["data"] = res

    return response


async def create(session: AsyncSession, user_id: int) -> Chat | None:
    chat = Chat(
        created_at=datetime.now(),
        uuid=str(uuid.uuid4()),
        user_id=user_id,
    )
    session.add(chat)
    await session.commit()
    return chat


async def get_chat_by_user_id(session: AsyncSession, user_id: int) -> Chat | None:
    stmt = (
        select(Chat)
        .filter(Chat.state != State.deleted.value)
        .filter(Chat.user_id == user_id)
    )
    result: Result = await session.execute(stmt)
    chat = result.scalars().first()
    return chat

async def select_by_id(session: AsyncSession, chat_id: int) -> Chat | None:
    stmt = (
        select(Chat)
        .filter(Chat.state != State.deleted.value)
        .filter(Chat.id == chat_id)
    )
    result: Result = await session.execute(stmt)
    chat = result.scalars().first()
    return chat


async def select_by_uuid(session: AsyncSession, chat_uuid: str) -> Chat | None:
    stmt = (
        select(Chat)
        .filter(Chat.state != State.deleted.value)
        .filter(Chat.uuid == chat_uuid)
    )
    result: Result = await session.execute(stmt)
    chat = result.scalars().first()
    return chat


async def update_chat(
        session: AsyncSession,
        chat: Chat,
        chat_update: ChatUpdate | ChatUpdatePartial,
        partial: bool = False,
) -> Chat:
    for name, value in chat_update.model_dump(exclude_unset=partial).items():
        setattr(chat, name, value)
    await session.commit()
    return chat


async def delete_chat(
        session: AsyncSession,
        chat: Chat,
) -> None:
    chat.state = State.deleted.value
    await session.commit()
