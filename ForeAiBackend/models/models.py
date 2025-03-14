from typing import Union, Any

from pydantic import BaseModel


class DocumentationCorpus(BaseModel):
    documentation_corpus: list[dict[str, Any]]
