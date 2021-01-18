import sys
from typing import Any, Collection, Dict, List, Optional, Union
from pydantic import BaseModel, create_model

from api.config import DEFAULT_TOP_K_READER, DEFAULT_TOP_K_RETRIEVER


class ModelDetails(BaseModel):
    id_model: str
    type_model: str


class QuestionAnswer(BaseModel):
    model_id: str
    question: str
    answer: str
    question_answer_id: int


class Question(BaseModel):
    questions: List[str]
    model_id: str
    filters: Optional[Dict[str, Optional[Union[str, List[str]]]]] = None
    top_k_reader: int = DEFAULT_TOP_K_READER
    top_k_retriever: int = DEFAULT_TOP_K_RETRIEVER


class Answer(BaseModel):
    answer: str
    score: int
    probability: int
    context: str
    offset_start: int
    offset_end: int
    offset_start_in_doc: int
    offset_end_int_doc: int
    document_id: str
    meta: create_model('Meta', name=(str, ...))


class Answers(BaseModel):
    query: str
    no_ans_gap: int
    answers: List[Answer]