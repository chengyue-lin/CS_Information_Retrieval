from elasticsearch import Elasticsearch

es=Elasticsearch([{'host':'localhost','port':9200}])
# es <Elasticsearch([{'host': 'localhost', 'port': 9200}])>
es = Elasticsearch(timeout= 600, hosts = "http://localhost:9200/")
#需创建index_mapping结构
#index_mapping = {

#}
print(es.ping())

#if es.indices.exists() is not True:
#    es.indices.create()


