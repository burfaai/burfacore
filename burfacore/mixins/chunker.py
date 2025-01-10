import re
from functools import cached_property
from typing import AsyncGenerator, Generator

from pyquery import PyQuery
from playwright.async_api import Page
from textblob import TextBlob, Sentence, WordList


class ChunkTextMixin:
    """_summary_"""

    def _split_oversized_sentence(
        self, tokens: WordList
    ) -> Generator[Sentence, None, None]:
        """
        Split a sentence that exceeds the context window into smaller chunks.

        Args:
            tokens (List[str]): List of words from the sentence

        Yields:
            Sentence: Chunked sentences that fit within context window
        """
        while tokens:
            chunk_tokens = tokens[: self.context_window]
            yield Sentence(" ".join(chunk_tokens))
            tokens = tokens[self.context_window :]

    def _filter_sentences(self, sentences: WordList) -> Generator[Sentence, None, None]:
        """
        Filter out sentences that are too short or too long.

        Args:
            sentences (WordList): List of words from the sentence

        Yields:
            Sentence: Filtered sentences
        """
        for sentence in sentences:
            if len(sentence) > 2:
                yield sentence

    def text_chunks(self, context: str) -> Generator[Sentence, None, None]:
        """_summary_: Queue Context"""
        current_chunk = Sentence("")
        sentences: Sentence = TextBlob(context).sentences
        for sentence in self._filter_sentences(sentences):
            for sized in self._split_oversized_sentence(sentence.words):
                while len(current_chunk.words) + len(sized.words) < self.context_window:
                    current_chunk = Sentence(" ") + sized + current_chunk
                yield current_chunk
                current_chunk = Sentence("")


class ChunkHTMLMixin(ChunkTextMixin):
    """_summary_"""

    DENIED_TAGS: set[str] = {"style", "script", "noscript"}
    DEFAULT_CHUNKER: str = "<h"

    @staticmethod
    def extract_section_title(section_content: PyQuery) -> str:
        """_summary_

        Args:
            section_content (PyQuery): _description_

        Returns:
            str: _description_
        """
        header_match = re.search(r"<h\d>(.*?)</h\d>", section_content.outer_html())
        if header_match:
            return PyQuery(header_match.group()).text()
        return section_content("p:first").text().split("\n", maxsplit=1)[0]

    @staticmethod
    def extract_links(section_content: PyQuery) -> dict[str, str]:
        """_summary_

        Args:
            section_content (PyQuery): _description_

        Returns:
            dict[str, str]: _description_
        """
        return {i.text(): i.attr("href") for i in section_content("a").items()}

    async def get_content(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        if "playwright_page" in self.response.meta:
            page: Page = self.response.meta["playwright_page"]
            return await page.content()
        return self.response.body

    @cached_property
    async def pq(self) -> PyQuery:
        """_summary_

        Returns:
            PyQuery: _description_
        """
        content = await self.get_content()
        pq = PyQuery(content)
        [pq.remove(tag) for tag in self.DENIED_TAGS]
        return pq

    async def chunks(self) -> AsyncGenerator:
        """_summary_

        Returns:
            AsyncGenerator: _description_

        Yields:
            Iterator[AsyncGenerator]: _description_
        """
        self._pq = await self.pq
        self.chunker = getattr(self, "chunker", self.DEFAULT_CHUNKER)

        sections = self._pq(self.info_selector).outer_html().split(self.chunker)

        for idx, section in enumerate(sections[1::], 1):
            section_content = PyQuery(f"{self.chunker}{section}")

            section_title = self.extract_section_title(section_content)
            section_links = self.extract_links(section_content)

            for cidx, chunk in enumerate(self.text_chunks(section_content.text())):
                chunk_links = {k: v for k, v in section_links.items() if k in chunk}
                yield (self._pq, idx, cidx, section_title, str(chunk), chunk_links)
