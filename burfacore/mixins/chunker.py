import re
from functools import cached_property
from typing import AsyncGenerator

from textblob import TextBlob, Sentence
from pyquery import PyQuery


class ChunkTextMixin:
    """_summary_"""

    def text_chunks(self, context: str = None) -> list[list[Sentence]]:
        """_summary_: Chunk Text"""
        blob = TextBlob(context)
        sentences = blob.sentences
        _chunks, _chunk = [], []

        for sentence in sentences:
            tokens = sentence.words

            if len(tokens) > self.context_window:
                raise ValueError("Sentence is too long")
            if len(tokens + _chunk) <= self.context_window:
                _chunk += [sentence]
            else:
                _chunks.append(_chunk)
                _chunk = [sentence]
        _chunks.append(_chunk)
        return _chunks


class ChunkHTMLMixin(ChunkTextMixin):
    """_summary_"""

    async def _get_pq(self, response) -> PyQuery:
        """_summary_"""
        if "playwright_page" in response.meta:
            page = response.meta["playwright_page"]
            content = await page.content()
        else:
            content = response.body
        return PyQuery(content)

    @cached_property
    async def pq(self) -> PyQuery:
        """_summary_: PyQuery Object"""
        _pq = await self._get_pq(self.response)
        return _pq.remove("script").remove("style").remove("noscript").remove("h1")

    async def chunks(self) -> AsyncGenerator[dict]:
        """_summary_: Chunk HTML 500 Word Context Window

        Yields:
            Generator[dict, None, None]: (Section Index, Chunk Index, Section Title, Chunk Text, Chunk Links)
        """
        _pq = await self.pq(self.info_selector)
        _tag = getattr(self, "chunker", "<h")
        sections = _pq.outer_html().split(_tag)

        for index, section in enumerate(sections[1::]):
            section_content = PyQuery(f"{_tag}{section}")

            header_search = re.search(r"<h\d>(.*?)</h\d>", section_content.outer_html())
            if header_search:
                section_title = PyQuery(header_search.group()).text()
            else:
                section_title = section_content("p:first").text()

            section_links = {
                i.text(): i.attr("href") for i in section_content("a").items()
            }
            section_chunks = self.text_chunks(section_content.text())

            for cindex, chunk in enumerate(section_chunks):
                chunk_text = " ".join([str(i) for i in chunk])
                chunk_links = {
                    k: v for k, v in section_links.items() if k in chunk_text
                }
                yield (self.pq, index, cindex, section_title, chunk_text, chunk_links)
