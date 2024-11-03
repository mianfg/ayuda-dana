"""ObjectID helper model."""

from typing import Annotated, Any, Callable

from bson import ObjectId
from pydantic import Field
from pydantic_core import core_schema


def ObjectIdField(*args, **kwargs):  # noqa: ANN002, ANN003, ANN201, D103, N802
    return Field(*args, **kwargs, format="objectid", examples=["507f1f77bcf86cd799439011"])


class _ObjectIdPydanticAnnotation:
    # Based on https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types.

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(input_value: str) -> ObjectId:
            try:
                return ObjectId(input_value)
            except Exception as e:
                raise ValueError("not a valid ObjectId, it must be a 24-character hex string") from e

        return core_schema.union_schema(
            [
                # check if it's an instance first before doing any further work
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
            serialization=core_schema.to_string_ser_schema(),
        )


class _OptionalObjectIdPydanticAnnotation:
    # Based on https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types.

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(input_value: str | None) -> ObjectId | None:
            if input_value is None:
                return None
            try:
                return ObjectId(input_value)
            except Exception as e:
                raise ValueError("not a valid ObjectId, it must be a 24-character hex string") from e

        return core_schema.union_schema(
            [
                # check if it's an instance first before doing any further work
                core_schema.is_instance_schema(ObjectId | None),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
            serialization=core_schema.to_string_ser_schema(),
        )


PyObjectId = Annotated[ObjectId, _ObjectIdPydanticAnnotation]
OptionalPyObjectId = Annotated[ObjectId, _OptionalObjectIdPydanticAnnotation]
