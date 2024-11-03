"""
UserModel.

Represents user information
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field
from pydantic_extra_types.coordinate import Coordinate

from ayuda_dana_backend.models.base import BackendBaseModel
from ayuda_dana_backend.models.objectid import ObjectIdField, PyObjectId
from ayuda_dana_backend.models.user import UserModel


class PetitionStatusModel(Enum):
    """Possible petition statuses."""

    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"


class PetitionModel(BackendBaseModel):
    """Represents a user in the system."""

    id: PyObjectId = ObjectIdField(description="Unique identifier for the user", alias="_id")  # A003
    createDate: datetime = Field(description="Timestamp indicating when the petition was created")  # noqa: N815
    updateDate: Optional[datetime] = Field(
        description="Timestamp indication when the petition as modified", default=None
    )  # noqa: N815
    user: UserModel = ObjectIdField(description="User that made petition")  # noqa: N815
    status: PetitionStatusModel = Field(description="Petition status", default=PetitionStatusModel.RED)
    description: str = Field(description="Petition description", default="")
    items: list[str] = Field(description="List of items in petition", default=[])
    location: Coordinate = Field(description="Petition coordinates")

    class Config:  # noqa: D106
        title = "User"
        json_schema_extra = {  # noqa: RUF012
            "description": ("Represents a petition."),
        }


class CreatePetitionModel(BackendBaseModel):
    """Create petition model."""

    status: PetitionStatusModel = Field(description="Petition status", default=PetitionStatusModel.RED)
    description: str = Field(description="Petition description", default="")
    items: list[str] = Field(description="List of items in petition", default=[])
    location: Coordinate = Field(description="Petition coordinates")


class SetPetitionStatusModel(BackendBaseModel):
    """Create petition model."""

    id: PyObjectId = ObjectIdField(description="Unique identifier for the user", alias="_id")  # A003
    status: PetitionStatusModel = Field(description="Petition status")
