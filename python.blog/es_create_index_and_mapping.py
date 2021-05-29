from requests_aws4auth import AWS4Auth
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
import uuid
from datetime import datetime, timezone, timedelta
import time
import random
import os

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

body = {
    "settings":{
        "analysis":{
            "tokenizer" : {
                "kuromoji_search_tokenizer" : {
                    "type" : "kuromoji_tokenizer",
                    "mode": "search"
                }
            },
            "analyzer" : {
                "kuromoji_search_analyzer" : {
                    "type" : "custom",
                    "tokenizer" : "kuromoji_search_tokenizer",
                    "char_filter": [
                        "icu_normalizer"                    
                    ],
                    "filter": [
                        "kuromoji_baseform",
                        "kuromoji_part_of_speech",
                        "cjk_width",
                        "kuromoji_stemmer",
                        "lowercase"
                    ]
                }
            }
        }
    },
    "mappings": {
        "doc": {
            "properties": {
                "content": {
                    "type": "string",
                    "analyzer": "kuromoji_search_analyzer"
                },
                "title": {
                    "type": "string",
                    "analyzer": "kuromoji_search_analyzer"
                },
                "category": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "tags": {
                    "type": "string",
                    "analyzer": "kuromoji_search_analyzer"
                },
                "date": {
                    "type": "date",
                    "format": "strict_date_optional_time||epoch_millis",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "ana": {
                            "type": "string",
                            "index": "analyzed"
                        }
                    }
                },
                "lank": {
                    "type": "long"
                }
            }
        }
    }
}

res = es.indices.create(index=INDEX, body=body)

print(res)
