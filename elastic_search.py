from elasticsearch import Elasticsearch
import os
from elasticsearch import helpers
import json
es=Elasticsearch([{'host':'localhost','port':9200}])

es = Elasticsearch(timeout= 600, hosts = "http://localhost:9200/")
#需创建index_mapping结构
#是否要创建 setting 函数？
index_mapping= {
        "mappings": {
                "document" : {
                        "properties":{
                                "title" :{
                                        'type' : 'text'
                                },
                                "date" : {
                                        'type' : 'text'
                                },
                                "keyword" : {
                                        'type' : 'text'
                                },
                                "source" : {
                                        'type' : 'text'
                                },
                                "link" : {
                                        'type' : 'text'
                                }
                        }
                }
        }
}

data =open(".json")   # input json file name
i =1
for q in data:   # input json file into the elastic search
        content = data.read()
        es.index(index='myindex', ignore=400, doc_type='doc', id=i, body=json.loads(content))
        i= i+1


#es.indices.create(index='first_one', ignore= 400)

#if es.indices.exists() is not True:
#    es.indices.create()


