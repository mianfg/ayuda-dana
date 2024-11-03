"""Base for all documents."""

from mongoengine import Document, EmbeddedDocument

from ayuda_dana_backend.services.database import check_dbrefs, to_dict


class BackendDocument(Document):
    """Backend base document."""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return to_dict(self)

    def check_dbrefs(self) -> bool:
        """Check if DBRefs are valid."""
        check_dbrefs(self)

        return True

    def save(self, check: bool = True, **kwargs) -> None:  # noqa: ANN003
        """Save new document."""
        if check:
            self.check_dbrefs()

        super().save(**kwargs)

    def update(self, check: bool = True, **kwargs) -> None:  # noqa: ANN003
        """Update document."""
        if check:
            for item in kwargs.values():
                if isinstance(item, (BackendDocument, BackendEmbeddedDocument)):
                    item.check_dbrefs()

        super().update(**kwargs)

    meta = {"abstract": True}  # noqa: RUF012


class BackendEmbeddedDocument(EmbeddedDocument):
    """Backend embedded document."""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return to_dict(self)

    def check_dbrefs(self) -> bool:
        """Check if DBRefs are valid."""
        check_dbrefs(self)

        return True

    meta = {"abstract": True}  # noqa: RUF012
