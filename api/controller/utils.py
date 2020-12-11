from api.controller import qa_models
from api.controller.es import conn as es_conn, get_model_ids_by_type
from api.controller.qa_models import QA_MODELS, DocQAModel, FaqQAModel
from api.config import FAQ_QA, DOC_QA

def initialize_existing_models():
    print("Called utils")
    doc_ids = get_model_ids_by_type(es_conn, DOC_QA)
    faq_ids = get_model_ids_by_type(es_conn, FAQ_QA)
    print("!\n\n!\n!\n\n!\n\n\n")
    print(doc_ids)
    for id in doc_ids:
       print("Initializing model with id:", id)
       model = DocQAModel(id, False)
       QA_MODELS[id] = model


    # for id in faq_ids:
    #     print("Initializeing model with id:", id)
    #     model = FaqQAModel(id, False)
    #     QA_MODELS[id] = model

