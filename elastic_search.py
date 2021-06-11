from elasticsearch import Elasticsearch
import os
import pandas as pd
from elasticsearch import helpers
import argparse
from clawer import *
import json
def main():
        parser= argparse.ArgumentParser(description="all args --url --pages --poolLen")
        parser.add_argument('--url', type=str)
        parser.add_argument('--pages', type=int)
        parser.add_argument('--poolLen', type=int)
        args= parser.parse_args()
        url=args.url
        pages = args.pages
        poolLen = args.poolLen
        crawl(url, pages, poolLen)

        es=Elasticsearch([{'host':'localhost','port':9200}])
        df = pd.read_json("data.json", lines=True)
        df2 = df.to_dict('records')
        print(df2[0])
        # es = Elasticsearch(timeout= 600, hosts = "http://localhost:9200/")
        #es.indices.delete(index='cs_172')  # delete the previous ont

        index_mapping= {
                "mappings": {
                        "properties": {
                                "content" : {
                                         'type' : 'text'
                                 },
                                "link" : {
                                        'type' : 'text'
                                 }
                        }
                }
        }

        my = es.indices.create(index='url_num', ignore= 400, body=index_mapping) #create a new index for the index_mapping function

        # data =open("data.json")   # input json file name
        def genera(df2):
                for c, line in enumerate(df2):
                        yield {
                                '_index' : 'url_num',
                                '_type': 'html',
                                '_id' : c,
                                '_source' : {
                                        'link' : line.get("url",None),
                                        'content' : line.get("text", None)
                                }
                        }
        mycustom = genera(df2)
        print(next(mycustom))
        res = helpers.bulk(es, genera(df2))
        '''
        for q in data:   # input json file into the elastic search    
                content = data.read()
                es.index(index='URL_num', ignore=400,  id=i, body=json.loads(content))
                i= i+1
        '''

        query = input("Please input what you want to search for query")  # user input

        result = es.search(index= 'url_num', body={
                "_source" : ["link"]
                ,"query": {
                        "match":{
                                "content": query

                        }
                }
        })

        print(result)

        #if es.indices.exists() is not True:
        #    es.indices.create()
if __name__=="__main__":
    main()


