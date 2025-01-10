from fastapi import APIRouter

from .auth.views import router as auth_router
from .chats.views import router as chats_router
from .messages.views import router as msg_router

router = APIRouter()

router.include_router(router=auth_router, prefix="/auth")
router.include_router(router=chats_router, prefix="/chats")
router.include_router(router=msg_router, prefix="/messages")
