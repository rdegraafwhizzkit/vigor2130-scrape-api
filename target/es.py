from elasticsearch import Elasticsearch
from json import dumps
import hashlib
from conf.config import config


def sha224(o, encoding='utf-8'):
    if type(o) == dict:
        return hashlib.sha224(dumps(o).encode(encoding)).hexdigest()
    elif type(o) == str:
        return hashlib.sha224(o.encode(encoding)).hexdigest()
    elif type(o) == int:
        return hashlib.sha224(str(o).encode(encoding)).hexdigest()
    elif type(o) == float:
        return hashlib.sha224(str(o).encode(encoding)).hexdigest()
    else:
        raise Exception('SHA224 for {} not found'.format(str(type(o))))


def index_objects(index, objects, doc_type='_doc', id_function=lambda x: sha224(x)):
    if type(objects) == dict:
        index_objects(index, [objects], doc_type, id_function)
    elif type(objects) == list:
        es = Elasticsearch(hosts=config['es']['hosts'])
        for o in objects:
            try:
                es.index(index=index, doc_type=doc_type, body=o, id=id_function(o))
            except Exception as ex:
                print('Could not index object {}: {}'.format(dumps(o), ex))
    else:
        raise Exception('Unable to load objects with type ' + str(type(objects)))
