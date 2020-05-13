from elasticsearch import Elasticsearch
from json import dumps
from conf.config import config
from helper.global_helpers import sha224


def index_objects(index, objects, doc_type='_doc', id_function=lambda x: sha224(x)):
    if type(objects) == dict:
        return index_objects(index, [objects], doc_type, id_function)
    elif type(objects) == list:
        es = Elasticsearch(hosts=config['es']['hosts'])
        for o in objects:
            try:
                es.index(index=index, doc_type=doc_type, body=o, id=id_function(o))
            except Exception as ex:
                print('Could not index object {}: {}'.format(dumps(o), ex))
        return len(objects)
    else:
        raise Exception('Unable to load objects with type ' + str(type(objects)))
