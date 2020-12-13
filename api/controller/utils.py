import logging

from api.controller.es import conn as es_conn, get_model_ids_by_type
from api.controller.models import ModelType, DocQAModel, FaqQAModel, MODELS

logger = logging.getLogger(__name__)

def initialize_existing_models():
    doc_ids = get_model_ids_by_type(es_conn, ModelType.doc_qa)
    faq_ids = get_model_ids_by_type(es_conn, ModelType.faq_qa)

    for id in doc_ids:
        logger.info(f"Initializing doc_qa model with id = {id}")
        model = DocQAModel(id, False)
        MODELS[id] = model

    for id in faq_ids:
        logger.info(f"Initializing faq_qa model with id = {id}")
        model = FaqQAModel(id, False)
        MODELS[id] = model
