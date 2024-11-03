from fastapi import APIRouter, Depends, HTTPException
from mongoengine import DoesNotExist

import ayuda_dana_backend.services.auth as auth_service
from ayuda_dana_backend.documents.petition import PetitionDocument
from ayuda_dana_backend.models.petition import CreatePetitionModel, PetitionModel, SetPetitionStatusModel
from ayuda_dana_backend.models.user import UserModel

router = APIRouter()


@router.post(
    "/new",
    response_description="Create petition",
    response_model=PetitionModel,
)
async def new(
    petition: CreatePetitionModel,
    user: UserModel = Depends(auth_service.get_logged_user),
):
    petition = PetitionDocument(
        user=user.id,
        status=petition.status,
        description=petition.description,
        items=petition.items,
        location={
            "latitude": petition.location.latitude,
            "longitude": petition.location.longitude,
        },
    )

    petition.save()

    return PetitionModel.model_validate(petition.to_dict())


@router.put(
    "/set-status",
    response_description="Set petition status",
    response_model=PetitionModel,
)
async def set_status(
    status: SetPetitionStatusModel,
    user: UserModel = Depends(auth_service.get_logged_user),
):
    try:
        petition = PetitionDocument.objects.get(id=status.id)
    except DoesNotExist as exc:
        raise HTTPException(404, str(exc))

    if petition.userId != user.id:
        raise HTTPException(
            403,
            "Cannot update petition as the request's user does not match the petition's user",
        )

    petition.update(set__status=status.status)

    return PetitionModel.model_validate(petition.to_dict())
