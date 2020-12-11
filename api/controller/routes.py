from starlette.responses import Response
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import UploadFile, File, Form

import os, logging
import shutil
import uuid
from pathlib import Path
from typing import Optional, List

from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.file_converter.txt import TextConverter

from rest_api.config import DB_HOST, DB_PORT, DB_USER, DB_PW, DB_INDEX, ES_CONN_SCHEME, TEXT_FIELD_NAME, \
    SEARCH_FIELD_NAME, FILE_UPLOAD_PATH, EMBEDDING_DIM, EMBEDDING_FIELD_NAME, EXCLUDE_META_DATA_FIELDS, VALID_LANGUAGES, \
    FAQ_QUESTION_FIELD_NAME, REMOVE_NUMERIC_TABLES, REMOVE_WHITESPACE, REMOVE_EMPTY_LINES, REMOVE_HEADER_FOOTER, \
    CREATE_INDEX, VECTOR_SIMILARITY_METRIC

from api.controller import es
from api.controller.models import ModelType, QA_MODELS
from api.controller.response import ModelDetails
from api.controller.request import Question
from api.controller.response import Answers
from api.app import app


logger = logging.getLogger(__name__)

@app.post("/test")
def test_route():
    return {'Hello': 'World'}


@app.post("/models/", status_code=201, response_model=ModelDetails)
def create_model(model_type: ModelType):
    try:
        model_data = es.add_model(es.conn, model_type)
    except Exception as e:
        raise HTTPException(status_code=400, details=str(e))

    return model_data


@app.get("/models/", response_model=List[ModelDetails])
def get_models_data():
    data = es.get_models_data(es.conn)

    return data

#
@app.post("/models/faq-qa/{model_id}/")
def add_question_answer(question: Question):
    return {
        'question': question,
        'answer': answer
    }
#

@app.post("/models/faq-qa/{model_id}/questions/")
def faq_qa_query(model_id: str, request: Question):
    if not model_id in QA_MODELS:
        raise HTTPException(status_code=404, 
            message=f"Couldn't find a model with id {model_id}. Available models: {list(QA_MODELS.keys())}")

    model = QA_MODELS[model_id]
    questions = request.questions
    results = []
    print(questions)
    for question in questions:
        result = model.finder.get_answers_via_similar_questions(
            question=question, top_k_retriever=request.top_k_retriever
        )
        results.append(result)

    return results


@app.post("/models/doc-qa/{model_id}/questions", response_model=Answers)
def doc_qa_query(model_id: str, request: Question):
    if not model_id in QA_MODELS:
        raise HTTPException(status_code=404, 
            message=f"Couldn't find a model with id {model_id}. Available models: {list(QA_MODELS.keys())}")

    model = QA_MODELS[model_id]
    questions = request.questions
    results = []

    for question in questions:
        result = model.finder.get_answers(question, top_k_retriever=request.top_k_retriever)
        results.append(result)

    return results


@app.post("/models/doc-qa/{model_id}/")
def upload_file(    
    file: UploadFile = File(...),
    remove_numeric_tables: Optional[bool] = Form(REMOVE_NUMERIC_TABLES),
    remove_whitespace: Optional[bool] = Form(REMOVE_WHITESPACE),
    remove_empty_lines: Optional[bool] = Form(REMOVE_EMPTY_LINES),
    remove_header_footer: Optional[bool] = Form(REMOVE_HEADER_FOOTER),
    valid_languages: Optional[List[str]] = Form(VALID_LANGUAGES)):
    
    try:
        file_path = Path(FILE_UPLOAD_PATH) / f"{uuid.uuid4().hex}_{file.filename}"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file.filename.split(".")[-1].lower() == "pdf":
            pdf_converter = PDFToTextConverter(
                remove_numeric_tables=remove_numeric_tables,
                remove_whitespace=remove_whitespace,
                remove_empty_lines=remove_empty_lines,
                remove_header_footer=remove_header_footer,
                valid_languages=valid_languages,
            )
            document = pdf_converter.convert(file_path)
        elif file.filename.split(".")[-1].lower() == "txt":
            txt_converter = TextConverter(
                remove_numeric_tables=remove_numeric_tables
            )
            document = txt_converter.convert(file_path)
        else:
            raise HTTPException(status_code=415, detail=f"Only .pdf and .txt file formats are supported.")

        document_to_write = {TEXT_FIELD_NAME: document["text"], "name": file.filename}
        #document_store.write_documents([document_to_write])
        #return "File upload was successful."
        return document_to_write
    finally:
        file.file.close()