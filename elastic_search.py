from elasticsearch import Elasticsearch
import os
from elasticsearch import helpers
import json
es=Elasticsearch([{'host':'localhost','port':9200}])

es = Elasticsearch(timeout= 600, hosts = "http://localhost:9200/")
es.indices.delete(index='cs_172')  # delete the previous ont
#需创建index_mapping结构
#是否要创建 setting 函数？
index_mapping= {
        "mappings": {
                "properties": {
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
my = es.indices.create(index='cs_172', ignore= [400,404], body=index_mapping) #create a new index for the index_mapping function
data =open(".json")   # input json file name
i =1
for q in data:   # input json file into the elastic search    (不知道对不对)
        content = data.read()
        es.index(index='cs_172', ignore=400,  id=i, body=json.loads(content))
        i= i+1
res = helpers.bulk()   #应该需要这个函数但不确定是否需要。如果需要如何用
query = input("Please input what you want to search for query")  #用户输入想要查询的query

result = es.search(index= 'cs_172', body={
        "query": {
                "march":{
                        "keyword": query       # 查找keyword中是否有一样的单词。不需要exact match

                }
        }
})

print(result)

#if es.indices.exists() is not True:
#    es.indices.create()


