from fastapi import APIRouter, Depends, HTTPException, Request

import ayuda_dana_backend.services.auth as auth_service
from ayuda_dana_backend.documents.user import UserDocument
from ayuda_dana_backend.models.user import UserModel

router = APIRouter()


@router.get("/auth")
async def auth() -> None:  # noqa: D103
    return None


@router.get("/login")
async def login():
    """Login to backend via Google SSO, will redirect to callback"""
    return await auth_service.login()


@router.get("/logout")
async def logout(user: UserModel = Depends(auth_service.get_logged_user)):
    """Logout and forget user session"""
    return await auth_service.logout("/docs")


@router.get("/callback")
async def login_callback(request: Request):
    """Retrieve callback from Google SSO, will establish session cookie"""
    openid, response = await auth_service.login_callback(request, "/docs")

    if not openid or not response:
        raise HTTPException(status_code=401, detail="Authentication failed")

    if openid and len(UserDocument.objects(googleId=openid.id)) == 0:
        # if so, we create a new user without preferences
        UserDocument(
            name=openid.display_name,
            email=openid.email,
            googleId=openid.id,
        ).save()

    if not response:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return response
