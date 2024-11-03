from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

import ayuda_dana_backend.services.auth as auth_service
from ayuda_dana_backend.documents.user import UserDocument
from ayuda_dana_backend.exceptions import InvalidReferenceException
from ayuda_dana_backend.models.user import SetUserPhoneModel, UserModel

router = APIRouter()


@router.post(
    "/phone",
    response_description="Set user phone",
    response_model=UserModel,
)
async def set_phone(
    phone: SetUserPhoneModel,
    user: UserModel = Depends(auth_service.get_logged_user),
):
    try:
        UserDocument.objects.get(id=user.id).update(set__phone=phone.phone)
    except InvalidReferenceException as exc:
        raise HTTPException(404, str(exc))
    except ValidationError as exc:
        raise HTTPException(400, str(exc))

    return UserModel(**UserDocument.objects.get(id=user.id).to_dict())


@router.get(
    "/",
    response_description="Get info from logged in user",
    response_model=UserModel,
)
async def user(user: UserModel = Depends(auth_service.get_logged_user)):
    return user
