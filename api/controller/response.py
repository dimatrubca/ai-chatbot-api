from typing import List
from pydantic import BaseModel, create_model

class ModelDetails(BaseModel):
    id_model: str
    type_model: str


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
    meta: create_model('Meta', name=(int, ...))

class Answers(BaseModel):
    query: str
    no_ans_gap: int
    answers: List[Answer]