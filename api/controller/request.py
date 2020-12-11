import sys
from typing import Any, Collection, Dict, List, Optional, Union

from pydantic import BaseModel

from api.config import DEFAULT_TOP_K_READER, DEFAULT_TOP_K_RETRIEVER


class Question(BaseModel):
    questions: List[str]
    top_k_reader: int = DEFAULT_TOP_K_READER
    top_k_retriever: int = DEFAULT_TOP_K_RETRIEVER