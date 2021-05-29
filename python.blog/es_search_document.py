import requests
from requests_aws4auth import AWS4Auth
import os
from elasticsearch import Elasticsearch, RequestsHttpConnection
import boto3
import json
from pprint import pprint

region = 'ap-northeast-1' 
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

ENDPOINT = os.environ.get('ENDPOINT')
INDEX = os.environ.get('INDEX')
TYPE = os.environ.get('TYPE')

region = 'ap-northeast-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key,
                   credentials.secret_key,
                   region,
                   service,
                   session_token=credentials.token)

HOST = ENDPOINT.replace('https://', '')

es = Elasticsearch(
    hosts=[{'host': HOST, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

query_simple = {
    "query": {
        "match": {
            "content": "Elasticsearch"
        }
    }
}
query_all_asc = {
    "query": {
        "match_all": {}
    },
    "sort": {
        "lank": {
            "order": "asc"
        }
    }
}
query_all_desc = {
    "query": {
        "match_all": {}
    },
    "sort": {
        "lank": {
            "order": "desc"
        }
    }
}
query_phrase = {
    "query": {
        "match_phrase": {
            "content": "証認"
        }
    }
}
query_highlight = {
    "query": {
        "match": {
            "content": {
                "query": "Cognito"
            }
        }
    },
    "highlight": {
        "fields": {
            "title": {},
            "content": {}
        }
    }
}
query_highlight = {
    "query": {
        "match": {
            "content": {
                "query": "Cognito"
            }
        }
    },
    "highlight": {
        "fields": {
            "content": {}
        }
    }
}
query_and = {
    "query": {
        "match": {
            "content": {
                "query": "Cognito Google",
                "operator": "and"
            }
        }
    }
}
query_or = {
    "query": {
        "match": {
            "content": {
                "query": "Cognito Google",
                "operator": "or"
            }
        }
    }
}
query_fuzzy = {
    "query": {
        "match": {
            "content": {
                "query": "Cognition",
                "fuzziness": 2
            }
        }
    }
}
query_sort_desc = {
    "query": {
        "match": {
            "content": {
                "query": "Elasticsearch"
            }
        }
    },
    "sort": {
        "lank": {
            "order": "desc"
        }
    }
}
query_sort_asc = {
    "query": {
        "match": {
            "content": {
                "query": "Elasticsearch"
            }
        }
    },
    "sort": {
        "lank": {
            "order": "asc"
        }
    }
}
query_multi_field = {
    "query": {
        "multi_match" : {
            "query": "Cognito", 
            "fields": [ "title", "content" ] 
        }
    }
}
query_boost = {
    "query": {
        "multi_match" : {
            "query": "Cognito", 
            "fields": [ "title", "content^10" ] 
        }
    }
}
query_full = {
    "query": {
        "multi_match" : {
            "query": "Cognito",
            "fuzziness": 2,
            "operator": "and",
            "fields": [ "title^10", "category^10", "tags^10", "content" ] 
        }
    },
    "sort": {
        "lank": {
            "order": "desc"
        }
    },
    "highlight": {
        "fields": {
            "title": {},
            "tags": {},
            "category": {},
            "content": {}
        }
    }
}

queries = (
#    query_simple,
#    query_all_asc,
#    query_all_desc,
#    query_phrase,
#    query_highlight,
#    query_and,
#    query_or,
#    query_fuzzy,
#    query_sort_desc,
#    query_sort_asc,
#    query_multi_field,
#    query_boost,
    query_full,
)

for query in queries:

    res = es.search(
        index=INDEX,
        doc_type=TYPE,
        body=query
    )
    
    pprint('----query----')
    
    pprint(query)
    
    pprint('----result----')
    
    pprint(res)
    
    '''
    for hit in res['hits']['hits']:
        if "highlight" in hit:
            pprint(hit["highlight"])
        pprint('{} {}'.format(hit["_source"]['title'], hit["_id"]))
    '''