# -*- coding: utf-8 -*-
import io
import json
import base64
import zipfile
from string import digits
from bs4 import BeautifulSoup
from .constants import DsaConstants


class Documents(DsaConstants):
    """Papers retrieved from Microsoft Academic API.

    Attributes
    ----------
    data: dict
        open-data file's content
    normalize_values: bool, defaults to True
        looks up values retrieved from html comment tags
        and replaces, e.g. "2" to "рішення".

    Usage
    -----
    >>> from dsa import Documents
    >>> docs = Documents.from_json("data/20210507000000_20210508000000.json", normalize_values=True)
    >>> docs.process_documents()
    >>> docs.save(json_file="test.json")
    >>> docs.save(jsonl_file="test.jsonl)
    """

    @classmethod
    def from_json(cls, json_file, normalize_values=True):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(data, normalize_values)

    def __init__(self, data, normalize_values=True):
        self.raw_data = data["items"]
        self.normalize_values = normalize_values
        self.processed_data = None

    def save(self, json_file=None, jsonl_file=None):
        if self.processed_data is None:
            raise ValueError("Process data first.")
        if json_file is None and jsonl_file is None:
            raise ValueError("Provide json/jsonl file paths.")
        if jsonl_file is not None:
            with open(jsonl_file, "w", encoding="utf-8") as f:
                for line in self.processed_data:
                    json.dump(line, f, ensure_ascii=False)
                    f.write("\n")
        if json_file is not None:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(
                    {"items": self.processed_data}, f, ensure_ascii=False, indent=4
                )

    def process_documents(self):
        self.processed_data = [*self.yield_records()]

    def yield_records(self):
        for document in self.raw_data:
            if "DOC_HTML" not in document:
                yield document
                continue
            yield from self.process_record(document)

    def process_record(self, record):
        html = self._extract_html(record["DOC_HTML"])
        metadata = self._extract_metadata(html)
        d = {**record, **metadata}
        d.pop("DOC_HTML")
        yield d

    def _extract_html(self, b64zip):
        base = base64.b64decode(b64zip)
        zip_archive = zipfile.ZipFile(io.BytesIO(base))
        html_filename = zip_archive.namelist()[0]
        html_content = zip_archive.read(html_filename)
        return BeautifulSoup(html_content, "html.parser")

    def _extract_metadata(self, soup):
        metadata = {}
        for item in soup.select("meta"):
            name, content = item.get("name"), item.get("content")
            if name is None:
                continue
            metadata[name] = (
                self._lookup_values(name, content) if self.normalize_values else content
            )
        return metadata

    def _lookup_values(self, name, values):
        remove_digits = str.maketrans("", "", digits)
        lookup_name = name.translate(remove_digits)
        return (
            Documents.MAPPINGS[lookup_name].get(values, values)
            if lookup_name in Documents.MAPPINGS.keys()
            else values
        )
