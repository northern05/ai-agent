from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Message, User
from app.core.models.message import Role


async def get_message_count(
        session: AsyncSession,
) -> int:
    stmt = select(func.count(Message.id)).filter(Message.role == Role.user)
    result = await session.execute(stmt)
    message_count = result.scalar()
    return message_count

async def get_unique_users_count(
        session: AsyncSession,
) -> int:
    stmt = select(func.count(User.id))
    result = await session.execute(stmt)
    user_count = result.scalar()
    return user_count