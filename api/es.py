import logging
from elasticsearch import Elasticsearch

from api.config import DB_HOST, DB_PORT


def connect_elasticsearch():
    _es = Elasticsearch([{'host': DB_HOST, 'port': DB_PORT}])
    if _es.ping():
        print('Connected to elasticsearch successfully!')
    else:
        print('Connection to elasticsearch failed!')
    return _es


def create_index(es_object, index_name, settings):
    created = False

    try:
        if not es_object.indices.exists(index_name):
            # ignore 400 -> ignore index already exists
            print(es_object.indices.create(index=index_name, ignore=400, body=settings))

        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


es = connect_elasticsearch()

# allowed type_model values: doc_qa, faq_qa
settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "created_model": {
            "properties": {
                "id_model": {
                    "type": "integer"
                },
                "type_model": {
                    "type": "string"
                }
            }
        }
    }
}

print(create_index(es, 'ai_models', settings))