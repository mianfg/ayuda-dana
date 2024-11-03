"""Petitions collection."""

import datetime

from mongoengine import (
    DateTimeField,
    EmbeddedDocumentField,
    EnumField,
    FloatField,
    ListField,
    ReferenceField,
    StringField,
)

from ayuda_dana_backend.documents.base import BackendDocument, BackendEmbeddedDocument
from ayuda_dana_backend.documents.user import UserDocument
from ayuda_dana_backend.models.petition import PetitionStatusModel


class PetitionLocationDocument(BackendEmbeddedDocument):
    """Petition location coordinates embedded document."""

    latitude = FloatField(required=True)
    longitude = FloatField(required=True)


class PetitionDocument(BackendDocument):
    """Petition document."""

    createDate = DateTimeField(  # noqa: N815
        default=datetime.datetime.now(tz=datetime.timezone.utc),
        required=True,
        db_field="createDate",
    )
    updateDate = DateTimeField(  # noqa: N815
        default=None,
        db_field="updateDate",
    )
    user = ReferenceField(UserDocument, required=True, dbref=True)  # noqa: N815
    status = EnumField(PetitionStatusModel, required=True)
    description = StringField(null=True, default=None)
    items = ListField(StringField(), null=True, default=None)
    location = EmbeddedDocumentField(PetitionLocationDocument, required=True)

    meta = {"collection": "petitions"}  # noqa: RUF012
