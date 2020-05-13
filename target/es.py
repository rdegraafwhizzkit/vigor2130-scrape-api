from elasticsearch import Elasticsearch, helpers
from conf.config import config
from helper.global_helpers import sha224


def index_objects(index, objects, doc_type='_doc', id_function=lambda x: sha224(x), hosts=None):
    if hosts is None:
        hosts = [{'host': 'localhost', 'port': 9200}]
    if type(objects) == dict:
        return index_objects(index, [objects], doc_type, id_function, hosts)
    elif type(objects) == list:
        es = Elasticsearch(hosts=hosts)
        for o in objects:
            o.update({
                '_id': id_function(o),
                '_type': doc_type,
                '_index': index
            })
        success, errors = helpers.bulk(
            es,
            objects
        )
        return success
    else:
        raise Exception('Unable to load objects with type ' + str(type(objects)))
