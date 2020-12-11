import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import elasticapm
from fastapi import APIRouter
from fastapi import HTTPException

from haystack import Finder
from rest_api.config import DB_HOST, DB_PORT, DB_USER, DB_PW, DB_INDEX, DEFAULT_TOP_K_READER, ES_CONN_SCHEME, \
    TEXT_FIELD_NAME, SEARCH_FIELD_NAME, EMBEDDING_DIM, EMBEDDING_FIELD_NAME, EXCLUDE_META_DATA_FIELDS, \
    RETRIEVER_TYPE, EMBEDDING_MODEL_PATH, USE_GPU, READER_MODEL_PATH, BATCHSIZE, CONTEXT_WINDOW_SIZE, \
    TOP_K_PER_CANDIDATE, NO_ANS_BOOST, READER_CAN_HAVE_NO_ANSWER, MAX_PROCESSES, MAX_SEQ_LEN, DOC_STRIDE, CONCURRENT_REQUEST_PER_WORKER, \
    FAQ_QUESTION_FIELD_NAME, EMBEDDING_MODEL_FORMAT, READER_TYPE, READER_TOKENIZER, GPU_NUMBER, NAME_FIELD_NAME, \
    VECTOR_SIMILARITY_METRIC, CREATE_INDEX, LOG_LEVEL

from rest_api.controller.request import Question
from rest_api.controller.response import Answers, AnswersToIndividualQuestion

from rest_api.controller.utils import RequestLimiter
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.reader.base import BaseReader
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.retriever.base import BaseRetriever
from haystack.retriever.sparse import ElasticsearchRetriever, ElasticsearchFilterOnlyRetriever
from haystack.retriever.dense import EmbeddingRetriever

from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.preprocessor.cleaning import clean_wiki_text

from rest_api.models import QAModel, FaqQAModel, DocQAModel
from rest_api.models import MODELS
from fastapi.responses import JSONResponse

logger = logging.getLogger('haystack')
logger.setLevel(LOG_LEVEL)

router = APIRouter()

# Init global components: DocumentStore, Retriever, Reader, Finder
doc_store = ElasticsearchDocumentStore(host=DB_HOST, port=DB_PORT, index="doc_test3")
retriever = ElasticsearchRetriever(document_store=doc_store)
reader = FARMReader(
    model_name_or_path=READER_MODEL_PATH,
    batch_size=BATCHSIZE,
    use_gpu=USE_GPU,
    num_processes=MAX_PROCESSES,
)  # type: Optional[BaseReader]
doc_dir = "data/rc"
# document_store = ElasticsearchDocumentStore()
dicts = convert_files_to_dicts(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
doc_store.write_documents(dicts)
FINDERS = {1: Finder(reader=reader, retriever=retriever)}
