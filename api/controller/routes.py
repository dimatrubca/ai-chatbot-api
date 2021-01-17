import os
import logging
import shutil
import uuid
from pathlib import Path
from typing import Optional, List

from starlette.responses import Response
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import UploadFile, File, Form, Body

from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.file_converter.txt import TextConverter
from haystack.preprocessor.preprocessor import PreProcessor

from api.config import  TEXT_FIELD_NAME, FILE_UPLOAD_PATH, VALID_LANGUAGES, REMOVE_NUMERIC_TABLES, REMOVE_WHITESPACE, REMOVE_EMPTY_LINES, REMOVE_HEADER_FOOTER
from api.controller import es
from api.controller.models import ModelType, MODELS
from api.controller.schemas import ModelDetails
from api.controller.schemas import Question
from api.controller.schemas import Answers
from api.app import app


logger = logging.getLogger(__name__)

@app.post("/test")
def test_route(model_id: str):
    print(es.delete_model(es.conn, model_id, MODELS))

    return {'Hello': 'World'}


@app.post("/models/", status_code=201, response_model=ModelDetails)
def create_model(model_type: ModelType):
    try:
        model_data = es.add_model(es.conn, model_type, MODELS)
    except Exception as e:
        raise HTTPException(status_code=400, details=str(e))

    return model_data


@app.get("/models/", response_model=List[ModelDetails])
def get_models_data():
    data = es.get_models_data(es.conn)

    return data


@app.post("/models/faq-qa/questions/")
def faq_qa_query(request: Question):
    model_id = request.model_id

    if not model_id in MODELS:
        raise HTTPException(status_code=404, 
            message=f"Couldn't find a model with id {model_id}. Available models: {list(MODELS.keys())}")

    model = MODELS[model_id]
    questions = request.questions
    results = []

    for question in questions:
        result = model.finder.get_answers_via_similar_questions(question=question)
        results.append(result)

    return results


@app.post("/models/doc-qa/questions")
def doc_qa_query(request: Question):
    model_id = request.model_id
    
    if not model_id in MODELS:
        raise HTTPException(status_code=404, 
            detail=f"Couldn't find a model with id {model_id}. Available models: {list(MODELS.keys())}")

    model = MODELS[model_id]
    questions = request.questions
    results = []

    for question in questions:
        result = model.finder.get_answers(question, top_k_retriever=request.top_k_retriever, top_k_reader=request.top_k_reader)
        results.append(result)

    return results


@app.post("/models/faq-qa/", status_code=200)
def add_question_answer(model_id: str, question: str, answer: str, question_answer_id: int):
    if model_id not in MODELS:
        raise HTTPException(status_code=400, detail="Invalid model id")

    retriever = MODELS[model_id].finder.retriever
    doc_store = retriever.document_store

    doc = {
        'question': question,
        'text': answer,
        'question_emb': retriever.embed_queries(texts=[question])[0],
        'question_answer_id': question_answer_id
    }

    doc_store.write_documents([doc])


@app.post("/models/doc-qa/")
def upload_file(    
    model_id: str = Form(...),
    file: UploadFile = File(...),
    remove_numeric_tables: Optional[bool] = Form(REMOVE_NUMERIC_TABLES)):

    print("uploading file")
    if model_id not in MODELS:
        raise HTTPException(status_code=400, detail="Invalid model id")
    
    try:
        file_path = Path(FILE_UPLOAD_PATH) / f"{uuid.uuid4().hex}_{file.filename}"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file.filename.split(".")[-1].lower() == "pdf":
            pdf_converter = PDFToTextConverter(
                remove_numeric_tables=remove_numeric_tables,
            )
            document = pdf_converter.convert(file_path)
        elif file.filename.split(".")[-1].lower() == "txt":
            txt_converter = TextConverter(
                remove_numeric_tables=remove_numeric_tables
            )
            document = txt_converter.convert(file_path)
        else:
            raise HTTPException(status_code=415, detail=f"Only .pdf and .txt file formats are supported.")

        processor = PreProcessor(clean_empty_lines=True,
                                clean_whitespace=True,
                                clean_header_footer=True,
                                split_by="word",
                                split_length=200,
                                split_respect_sentence_boundary=True)
        docs = processor.process(document)

        # Add name field to documents
        for doc in docs:
            doc['name'] = file.filename

        doc_store = MODELS[model_id].finder.retriever.document_store
        doc_store.write_documents(docs)

        return docs
    finally:
        file.file.close()


@app.delete("/models/doc-qa/", status_code=200)
def delete_file(model_id: str, filename: str):
    es.conn.delete_by_query(index=model_id, doc_type='_doc', body={ 'query': { 'match': { 'name': filename  } }})
        

@app.delete("/models/faq-qa", status_code=200)
def delete_question_answer(model_id: str, question_answer_id: int):
    es.conn.delete_by_query(index=model_id, doc_type='_doc', body={"query": { "bool": {"must": [{"match": {"question_answer_id": answer}}]}}})


@app.delete("/models")
def delete_model(model_id: str, status_code=200):
    es.delete_model(es.conn, model_id, MODELS)


@app.put("models/faq-qa", status_code=200)
def modify_question_answer(model_id: str, new_answer: str, question_answer_id: str):
     q = {
        "script": {
            f"inline": "ctx._source.text = '{new_answer}'",
            "lang": "painless"
        },
        "query": {
            "match": {
            "question_answer_id": "3"
            }
        }
    }

    es.update_by_query(body=q,doc_type='_doc', index=model_id)