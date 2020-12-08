from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.base import BaseRetriever
from haystack.retriever.sparse import ElasticsearchRetriever, ElasticsearchFilterOnlyRetriever
from haystack.retriever.dense import EmbeddingRetriever
from haystack.reader.farm import FARMReader
from haystack import Finder
from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.preprocessor.cleaning import clean_wiki_text
#from api.controller.request import Question
from api.config import DB_HOST, DB_PORT, DB_INDEX

import requests


QA_MODELS = {}

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
    def __init__(self, add_sample_data=False):
        QAModel.__init__(self)

        doc_store = ElasticsearchDocumentStore(host=DB_HOST, port=DB_PORT, index=DB_INDEX + str(self.id))
        dicts = convert_files_to_dicts(dir_path="data/rc", clean_func=clean_wiki_text, split_paragraphs=True)
        doc_store.write_documents(dicts)
        retriever = ElasticsearchRetriever(document_store=doc_store)
        reader = FARMReader("deepset/roberta-base-squad2", use_gpu=False)
        
        self.finder = Finder(reader, retriever)

        if add_sample_data:
            add_sample_data_doc_qa(self)


class FaqQAModel(QAModel):
    def __init__(self, add_sample_data=False):
        QAModel.__init__(self)

        doc_store = ElasticsearchDocumentStore(host=DB_HOST, port=DB_PORT, index=DB_INDEX + str(self.id)) 
        retriever = EmbeddingRetriever(document_store=doc_store, embedding_model="deepset/sentence_bert", use_gpu=False)

        self.finder = Finder(reader=None, retriever=retriever)

        if add_sample_data:
            add_sample_data_faq_qa(self)


def add_sample_data_doc_qa(model: DocQAModel):
    dicts = convert_files_to_dicts(dir_path="data/rc", clean_func=clean_wiki_text, split_paragraphs=True)
    model.finder.retriever.document_store.write_documents(dicts)

        
def add_sample_data_faq_qa(model: FaqQAModel):
    df = pd.read_csv("data/small_faq_covid.csv")
    df.fillna(value="", inplace=True)
    df["question"] = df["question"].apply(lambda x: x.strip())
    
    self.finder = Finder(reader=None, retriever=retriever)

    # Get embeddings for our questions from the FAQs
    questions = list(df["question"].values)
    df["question_emb"] = retriever.embed_queries(texts=questions)
    df = df.rename(columns={"answer": "text"})

    # Convert Dataframe to list of dicts and index them in our DocumentStore
    docs_to_index = df.to_dict(orient="records")
    document_store.write_documents(docs_to_index)
    model.finder.retriever.document_store.write_documents(docs_to_index)