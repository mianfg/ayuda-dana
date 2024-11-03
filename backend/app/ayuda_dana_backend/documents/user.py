"""Users collection."""

import datetime

from mongoengine import (
    DateTimeField,
    EmailField,
    StringField,
)

from ayuda_dana_backend.documents.base import BackendDocument


class UserDocument(BackendDocument):
    """User document."""

    createDate = DateTimeField(  # noqa: N815
        default=datetime.datetime.now(tz=datetime.timezone.utc),
        required=True,
        db_field="createDate",
    )
    name = StringField(required=True)
    email = EmailField(required=True)
    googleId = StringField(required=True)  # noqa: N815
    phone = StringField(null=True, default=None)

    meta = {"collection": "users"}  # noqa: RUF012
