from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from datetime import datetime
from elasticsearch_dsl.connections import connections


es = Elasticsearch([{'host':'202.112.51.162','port':9200}])


def loadData(table,sources=[],detail={}):
    query = {
        "sort": ["_doc"],
        "_source":sources,
    }
    query.update(detail)
    page = es.search(index=table, size=10000, scroll='2m', body=query)
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']
    while scroll_size > 0:
        page = es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])
        yield page['hits']['hits']




