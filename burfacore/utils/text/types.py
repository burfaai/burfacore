from functools import cached_property
from pydantic import Field, computed_field
from burfacore.core.schema import BurfaBase
from burfacore.mixins.text import BaseTextMixin, TextEmbeddingMixin, TextEntityMixin


class Chunk(BurfaBase, BaseTextMixin, TextEntityMixin, TextEmbeddingMixin):
    """_summary_: Base Class for Chunking Data"""

    title: str = Field(
        ...,
        title="Chunk Title",
        description="Title of the chunk",
        example="Introduction",
    )
    number: int | float = Field(
        ...,
        title="Chunk Number",
        description="Number of the chunk",
        example=1,
    )
    content: str = Field(
        ...,
        title="Chunk Content",
        description="Content of the chunk",
        example="This is the introduction",
    )

    @cached_property
    def text(self) -> str:
        """_summary_: Chunk Text"""
        return self.content

    @computed_field
    @property
    def embeddings(self):
        """_summary_: Chunk Embeddings"""
        return self.embeddings_

    @computed_field
    @property
    def keywords(self):
        """_summary_: Chunk Keywords"""
        return self.keywords_()
