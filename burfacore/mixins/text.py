from abc import abstractmethod
from functools import cached_property
import numpy as np

from pydantic import computed_field

import nltk
from textblob import TextBlob
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


class TextMixin:
    """_summary_"""

    @abstractmethod
    @cached_property
    def blob(self) -> TextBlob:
        """_summary_"""
        raise NotImplementedError("Method not implemented")

    @cached_property
    def stripped(self) -> str:
        """_summary_"""
        text_ = self.blob.raw.strip().split()
        text = " ".join([i.strip().lower() for i in text_])
        return TextBlob(text).stripped

    @computed_field
    @property
    def entities(self) -> list[dict]:
        """_summary_"""
        _entities = nltk.ne_chunk(self.blob.tags)
        return list(
            filter(
                lambda e: isinstance(e["entity"], nltk.Tree),
                map(
                    lambda entity: dict(entity=entity, pos=_entities.index(entity)),
                    _entities,
                ),
            )
        )

    @computed_field
    @property
    def entropy(self) -> float:
        """_summary_"""
        return np.sum(
            [
                -i / len(self.stripped) * np.log2(i / len(self.stripped))
                for i in np.unique(list(self.stripped), return_counts=True)[1]
            ]
        )

    @computed_field
    @property
    def embeddings(self) -> dict[str, list[float | list[float]]]:
        """_summary_"""
        _embeddings = model.encode(
            self.blob.correct().stripped,
            output_value=None,
            # TODO: Full Embeddings in Production
        )
        return {
            k: _embeddings.get(k).tolist()
            for k in ["token_embeddings", "sentence_embedding"]
        }

    @computed_field
    @property
    def compact_summary(self) -> str:
        """_summary_"""
        # TODO: Implement Custom Summarizer with Agent
        return "Summary Here"
