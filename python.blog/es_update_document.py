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

document = {
    "doc":{
        'lank': 10
    }
}

ID = '83788a6c-bf51-11eb-b1a2-0ace6787327c'

res = es.update(
    index=INDEX, 
    id=ID, 
    body=json.dumps(document), 
    doc_type=TYPE
)

print(res)

