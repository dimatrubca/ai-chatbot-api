from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.base import BaseRetriever
from haystack.retriever.sparse import ElasticsearchRetriever, ElasticsearchFilterOnlyRetriever
from haystack.retriever.dense import EmbeddingRetriever
from haystack.reader.farm import FARMReader
from haystack import Finder
from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.preprocessor.cleaning import clean_wiki_text
from rest_api.controller.request import Question
from rest_api.config import DB_HOST, DB_PORT, DB_INDEX


MODELS = {}

class QAModel:
    _counter = 0

    def __init__(self):
        QAModel._counter += 1
        self.id = QAModel._counter
        self.finder = None

        MODELS[self.id] = self


    def document_store(self):
        return self.finder.retriever.document_store


class DocQAModel(QAModel):
    def __init__(self):
        QAModel.__init__(self)

        doc_store = ElasticsearchDocumentStore(host=DB_HOST, port=DB_PORT, index=DB_INDEX + str(self.id))
        dicts = convert_files_to_dicts(dir_path="data/rc", clean_func=clean_wiki_text, split_paragraphs=True)
        doc_store.write_documents(dicts)
        retriever = ElasticsearchRetriever(document_store=doc_store)
        reader = FARMReader("deepset/roberta-base-squad2", use_gpu=False)
        
        self.finder = Finder(reader, retriever)


class FaqQAModel(QAModel):
    def __init__(self):
        QAModel.__init__(self)

        doc_store = ElasticsearchDocumentStore(host=DB_HOST, port=DB_PORT, index=DB_INDEX + str(self.id)) 
        retriever = EmbeddingRetriever(document_store=doc_store, embedding_model="deepset/sentence_bert", use_gpu=False)
        
        self.finder = Finder(reader=None, retriever=retriever)

