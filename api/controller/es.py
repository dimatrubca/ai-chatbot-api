import logging
from pprint import pprint
from random import randint
from elasticsearch import Elasticsearch

from api.config import DB_HOST, DB_PORT, FAQ_QA, DOC_QA, LOG_LEVEL


logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def connect_elasticsearch() -> Elasticsearch:
    _es = Elasticsearch([{'host': DB_HOST, 'port': DB_PORT}])
    if _es.ping():
        logger.info('Connected to elasticsearch successfully!')
    else:
        logger.error('Connection to elasticsearch failed!')

    return _es


def create_index(es_object: Elasticsearch, index_name: str, settings: dict) -> bool:
    created = False

    try:
        if not es_object.indices.exists(index_name):
            # ignore 400 -> ignore index already exists
            res = es_object.indices.create(index=index_name, ignore=400, body=settings)
            logger.info(f'Create index {index_name} response: {res}')

        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def add_record(es_object: Elasticsearch, index_name: str, record: dict):
    try:
        outcome = es_object.index(index=index_name, body=record)
        logger.info(f'Add record', outcome)
    except Exception as e:
        logger.error(str(e))


def add_model(es_object: Elasticsearch, model_type: str = FAQ_QA):
    record = {
        'id_model': model_type + str(randint(1, 1000000000000)),
        'type_model': model_type
    }

    add_record(es_object, 'ai_models', record)


def search(es_object: Elasticsearch, index_name: str, search: dict):
    res = es_object.search(index=index_name, body=search)
    hits = res['hits']['hits']
    
    return hits


def get_models_data(es_object: Elasticsearch, match_query=None):
    if not match_query:
        match_query = {'query': {'match_all': {}}}

    hits = search(es_object, 'ai_models', match_query)
    models = []

    for hit in hits:
        models.append({
            'id_model': hit['_source']['id_model'],
            'type_model': hit['_source']['type_model']
        })

    return models


def get_model_ids_by_type(es_object: Elasticsearch, model_type=FAQ_QA):
    match_query = { "query": { "match" : { "type_model": model_type }}}

    data = get_models_data(es_object, match_query)
    ids = [x['id_model'] for x in data]

    return ids

es = connect_elasticsearch()

# allowed type_model values: doc_qa, faq_qa
settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "id_model": { "type": "keyword"},
            "type_model": { "type": "keyword"}
        }
    }
}

create_index(es, 'ai_models', settings)

#add_record(es, 'ai_models', rec1)
#add_model(es, DOC_QA)
#add_model(es, FAQ_QA)

search_object = {'query': {'match_all': {}}}
search(es, 'ai_models', search_object)

pprint(get_models_data(es))
pprint(get_model_ids_by_type(es, DOC_QA))

#add_record(es, 'ai_models', rec1)