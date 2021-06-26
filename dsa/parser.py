import io
import json
import base64
import zipfile
from copy import deepcopy
from string import digits
from bs4 import BeautifulSoup
from .constants import DsaConstants


class Documents(DsaConstants):
    
    @classmethod
    def from_json(cls, json_file, remap=True):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(data, remap)

    def __init__(self, data, remap=True):
        self.data = data
        self.remap = remap
        self.processed = None

    def process(self):
        self.processed = deepcopy(self.data)
        for document in self.processed["items"]:
            if "DOC_HTML" not in document:
                continue
            html = self._extract_html(document["DOC_HTML"])
            metadata = self._extract_metadata(html)
            document.update(metadata)
            document.pop("DOC_HTML")

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
            remove_digits = str.maketrans("", "", digits)
            lookup_name = name.translate(remove_digits)
            if self.remap:
                metadata[name] = (
                    Documents.MAPPINGS[lookup_name].get(content, content)
                    if lookup_name in Documents.MAPPINGS.keys()
                    else content
                )
            else:
                metadata[name] = content
        return metadata
