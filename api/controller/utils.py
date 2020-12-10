from api.controller import qa_models
from api.controller.es import es, get_model_ids_by_type
from api.controller.qa_models import QA_MODELS, DocQAModel, FaqQAModel
from config import FAQ_QA, DOC_QA

def initialize_existing_models():
    doc_ids = get_model_ids_by_type(es, FAQ_QA)
    faq_ids = get_model_ids_by_type(es, DOC_QA)

    for id in doc_ids:
        full_id = DOC_QA + id
        model = DocQAModel(full_id, False)
        QA_MODELS[full_id] = model

    for id in faq_ids:
        full_id = FAQ_QA + id
        model = FaqQAModel(full_id, False)
        QA_MODELS[full_id] = model

