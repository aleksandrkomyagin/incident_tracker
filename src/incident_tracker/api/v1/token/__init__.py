from fastapi import APIRouter

from .create_token import create_token_router
from .refresh_token import refresh_router
from .revoke_token import revoke_router

token_router = APIRouter(prefix="/token", tags=["tokens"])

token_router.include_router(create_token_router)
token_router.include_router(refresh_router)
token_router.include_router(revoke_router)
