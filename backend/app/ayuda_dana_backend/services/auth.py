import datetime  # to calculate expiration of the JWT

from fastapi import Request, Security
from fastapi.responses import RedirectResponse
from fastapi.security import (
    APIKeyCookie,  # this is the part that puts the lock icon to the docs
)
from fastapi_sso.sso.base import OpenID
from fastapi_sso.sso.google import GoogleSSO
from jose import jwt

from ayuda_dana_backend.documents.user import UserDocument
from ayuda_dana_backend.models.user import UserModel

SECRET_KEY = ""  # used to sign JWTs, make sure it is really secret
CLIENT_ID = ""
CLIENT_SECRET = ""

sso = GoogleSSO(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://localhost:9999/v1/auth/callback",
)


async def get_logged_user(cookie: str = Security(APIKeyCookie(name="token"))) -> OpenID:
    """Get user's JWT stored in cookie 'token', parse it and return the user's OpenID."""
    claims = jwt.decode(cookie, key=SECRET_KEY, algorithms=["HS256"])
    open_id = OpenID(**claims["pld"])
    user = UserModel(**UserDocument.objects.get(googleId=open_id.id).to_dict())
    return user


async def login():
    """Redirect the user to the Google SSO login page"""
    with sso:
        return await sso.get_login_redirect()


async def logout(url: str):
    """Forget the user's session"""
    response = RedirectResponse(url=url)
    response.delete_cookie(key="token")
    return response


async def login_callback(request: Request, redirect_url: str):
    """Process login and redirect user to a certain endpoint"""
    with sso:
        openid = await sso.verify_and_process(request)
        if not openid:
            return None

    # Create a JWT with the user's OpenID
    expiration = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)
    token = jwt.encode(
        {"pld": openid.dict(), "exp": expiration, "sub": openid.id},
        key=SECRET_KEY,
        algorithm="HS256",
    )

    response = RedirectResponse(url=redirect_url)
    response.set_cookie(key="token", value=token, expires=expiration)
    return openid, response
