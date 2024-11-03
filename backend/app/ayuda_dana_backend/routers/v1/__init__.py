from fastapi import APIRouter

from ayuda_dana_backend.routers.v1.auth import router as auth_api
from ayuda_dana_backend.routers.v1.petition import router as petition_api
from ayuda_dana_backend.routers.v1.user import router as user_api

router = APIRouter()

router.include_router(auth_api, prefix="/auth", tags=["auth"])
router.include_router(user_api, prefix="/user", tags=["user"])
router.include_router(petition_api, prefix="/petition", tags=["petition"])
