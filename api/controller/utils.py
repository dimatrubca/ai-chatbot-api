import logging

from api.controller.es import conn as es_conn, get_model_ids_by_type
from api.config import FAQ_QA, DOC_QA
from api.controller.model_wrappers import QA_MODELS, DocQAWrapper, FaqQAWrapper

logger = logging.getLogger(__name__)

def initialize_existing_models():
    doc_ids = get_model_ids_by_type(es_conn, DOC_QA)
    faq_ids = get_model_ids_by_type(es_conn, FAQ_QA)

    for id in doc_ids:
        logger.info(f"Initializing doc_qa model with id = {id}")
        model = DocQAWrapper(id, False)
        QA_MODELS[id] = model

    for id faq_ids:
        logger.info(f"Initializing faq_qa model with id = {id}")
        model = FaqQAWrapper(id, False)
        QA_MODELS[id] = model