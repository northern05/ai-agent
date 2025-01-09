from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User


async def add_user(session: AsyncSession, wallet: str) -> User | None:
    user = User(wallet=wallet)
    session.add(user)
    await session.commit()
    return user


async def select_by_wallet(session: AsyncSession, wallet: str) -> User | None:
    stmt = (
        select(User)
        .where(User.wallet == wallet)
    )

    result = await session.execute(stmt)
    user: User | None = result.scalars().first()
    return user