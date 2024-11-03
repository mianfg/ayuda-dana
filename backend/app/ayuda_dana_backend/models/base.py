"""Base model."""

from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict


class BackendBaseModel(BaseModel):
    """
    Base model for backend.

    Encapsulates common configuration for all models
    """

    model_config = ConfigDict(
        # whether to validate the data when the model is changed
        validate_assignment=True,
        # forbid any extra attributes during model initialization
        # to enforce schema on construction
        extra="ignore",
        exclude_unset=True,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        },
    )

    @classmethod
    def from_mongo(cls, data: dict):  # noqa: ANN206
        """We must convert _id into "id"."""
        if not data:
            return data
        id = data.pop("_id", None)  # noqa A003
        return cls(**dict(data, id=id))

    def mongo(self, **kwargs):  # noqa: ANN201
        """Convert to mongo-parseable dictionary."""
        exclude_unset = kwargs.pop("exclude_unset", True)
        by_alias = kwargs.pop("by_alias", True)

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )

        # Mongo uses `_id` as default key. We should stick to that as well.
        if "_id" not in parsed and "id" in parsed:
            parsed["_id"] = parsed.pop("id")

        return parsed
