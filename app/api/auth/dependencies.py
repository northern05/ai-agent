import json

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.modules_factory import redis_db
from app.core.models import db_helper, User
from . import crud
from app.core.config import COOKIE_SESSION_ID_KEY

async def extract_user_from_access_token(
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY, default=None),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have to first sign_in",
        )

    session_info_str = await redis_db.get(session_id)
    if not session_info_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have to first sign_in",
        )
    session_info = json.loads(session_info_str)
    if not session_info or not session_info.get('siwe'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have to first sign_in",
        )

    # expires = COOKIES[session_id]['expires']

    address = session_info['siwe'].get("address")


    user = await crud.select_by_wallet(session=session, wallet=address)
    if not user:
        # logging.warning(f"Not found user by wallet: {address}")
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        user = await crud.add_user(session=session, wallet=address)
    return user