from functools import cached_property
import numpy as np

import nltk
from textblob import TextBlob
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def _get_blob(text: str) -> TextBlob:
    """_summary_: TextBlob Object"""
    _norm = " ".join([i.strip() for i in text.strip().split()])
    return TextBlob(_norm)


class BaseTextMixin:
    """_summary_: A Base Class for Text Processing Functions"""

    @cached_property
    def blob(self) -> TextBlob:
        """_summary_: TextBlob Object"""
        return _get_blob(self.context)

    @cached_property
    def stripped_(self) -> str:
        """_summary_"""
        return self.blob.stripped

    @cached_property
    def tokens_(self) -> list[str]:
        """_summary_"""
        return self.blob.words

    @cached_property
    def sentences_(self) -> list[str]:
        """_summary_"""
        return [str(i) for i in self.blob.sentences]


class TextFeaturesMixin:
    """_summary_"""

    @cached_property
    def blob(self) -> TextBlob:
        """_summary_: TextBlob Object"""
        return _get_blob(self.context)

    @cached_property
    def normalized_text_(self) -> str:
        """_summary_: Normalized Text Data"""
        return " ".join(self.blob.tokens)

    @cached_property
    def token_count_(self) -> int:
        """_summary_"""
        return len(self.blob.tokens)

    @cached_property
    def sentence_count_(self) -> int:
        """_summary_"""
        return len(self.blob.sentences)

    @cached_property
    def entropy_(self) -> float:
        """_summary_"""
        return np.sum(
            [
                -i
                / len(self.normalized_text_)
                * np.log2(i / len(self.normalized_text_))
                for i in np.unique(list(self.normalized_text_), return_counts=True)[1]
            ]
        )


class TextEntityMixin:
    """_summary_"""

    @cached_property
    def blob(self) -> TextBlob:
        """_summary_: TextBlob Object"""
        _raw = self.raw.replace("\n", " ").replace("\xa0", " ")
        return _get_blob(_raw)

    @cached_property
    def keywords_(self) -> list[str]:
        """_summary_"""
        _keywords = {
            token: self.blob.words.count(token) / (self.blob.words.index(token) + 1)
            for token in set(
                [i[0] for i in nltk.pos_tag(self.blob.words) if i[1].startswith("N")]
            )
        }
        return dict(sorted(_keywords.items(), key=lambda x: x[1], reverse=True))

    @cached_property
    def entities_(self) -> list[dict]:
        """_summary_"""
        return list(
            map(
                lambda e: dict(
                    label=e.label().lower(),
                    entity=" ".join(i[0] for i in e.leaves()).lower(),
                ),
                filter(
                    lambda chunk: isinstance(chunk, nltk.Tree),
                    nltk.ne_chunk(self.blob.tags),
                ),
            )
        )


class TextEmbeddingMixin:
    """_summary_"""

    @cached_property
    def blob(self) -> TextBlob:
        """_summary_: TextBlob Object"""
        return _get_blob(self.context)

    def embeddings_(self, *args, **kwargs) -> dict[str, list[float | list[float]]]:
        """_summary_"""
        _embeddings = model.encode(
            " ".join(self.blob.words),
            output_value=None,
            # TODO: Full Embeddings in Production
        )
        return {
            k: _embeddings.get(k).tolist()
            for k in ["token_embeddings", "sentence_embedding"]
        }


class TextSummaryMixin:
    """_summary_"""

    def summary_(self, *args, **kwargs) -> str:
        """_summary_"""
        # TODO: Implement Custom Summarizer with Agent
        return "I will set up a custom summarizer soon"
