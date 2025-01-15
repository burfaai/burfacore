from io import BytesIO
from pydantic import Field, FilePath, AnyHttpUrl, computed_field

from burfacore.core.types import DatasetType, DatabaseFormat
from burfacore.core.schema import BurfaBase


class Document(BurfaBase):
    """_summary_: Document Class"""

    source: AnyHttpUrl | FilePath = Field(
        title="Document Source",
        description="Document Source URL",
        example="https://example.com/document.pdf",
    )
    document_type: DatasetType = Field(
        title="Document Type",
        description="Document Type",
        example="document",
    )
    document_format: DatabaseFormat = Field(
        title="Document Format",
        description="Document Format",
        example="pdf",
    )
    name: str = Field(
        title="Document Name",
        description="Document Name",
        example="document.pdf",
    )

    @computed_field
    @property
    def file(self) -> BytesIO:
        """_summary_: File Object"""
        raise NotImplementedError("Method not implemented")

    @computed_field
    @property
    def content(self) -> list[str]:
        """_summary_: Document Content"""
        raise NotImplementedError("Method not implemented")
