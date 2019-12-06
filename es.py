from elasticsearch import Elasticsearch
from json import loads
import hashlib
import glob

es = Elasticsearch()

for file in [f for f in glob.glob('data/*.json', recursive=False)]:
    print(file)
    with open(file, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip()
            try:
                res = es.index(
                    index="vigor2130",
                    doc_type='_doc',
                    body=loads(line),
                    id=hashlib.sha224(line.encode('utf-8')).hexdigest()
                )
            except:
                print(line)
            line = f.readline()
