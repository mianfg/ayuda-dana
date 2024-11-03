"""
UserModel.

Represents user information
"""

from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from ayuda_dana_backend.models.base import BackendBaseModel
from ayuda_dana_backend.models.objectid import ObjectIdField, PyObjectId


class UserModel(BackendBaseModel):
    """Represents a user in the system."""

    id: PyObjectId = ObjectIdField(description="Unique identifier for the user", alias="_id")  # A003
    createDate: datetime = Field(description="Timestamp indicating when the user was created")  # noqa: N815
    name: str = Field(description="Name of user")
    email: EmailStr = Field(description="Email of user")
    googleId: str = Field(description="Unique identifier in login auth provider")  # A003  # noqa: N815
    phone: Optional[PhoneNumber] = Field(description="Phone number of user", default=None)

    class Config:  # noqa: D106
        title = "User"
        json_schema_extra = {  # noqa: RUF012
            "description": ("Represents a user in the system.\n\nThis model contains all the user information."),
        }


class SetUserPhoneModel(BackendBaseModel):
    """Setter: user phone."""

    phone: PhoneNumber = Field(description="User phone number")
