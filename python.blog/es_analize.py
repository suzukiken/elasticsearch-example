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

word = "東京スカイツリーと関西国際空港で少々アブラカダブラをする"
word = "東京都葛飾区森之宮ヒルズ999号室フィグメントリサーチ田代和義"
word = "AWSのElasticsearch Serviceを使っていて、Googleで開発者向けの情報を検索するとElastic.coのサイトが引っかかるのでそちらでドキュメントを見ることが多い。"

items = [
    {
        "analyzer": "kuromoji_search_analyzer",
        "text": word
    }, {
        "analyzer": "kuromoji_normal_analyzer",
        "text": word
    }, {
        "analyzer": "kuromoji_extended_analyzer",
        "text": word
    }, {
        "text": word
    } 
]

for item in items:

    res = es.indices.analyze(
        index=INDEX, 
        body=json.dumps(item)
    )

    pprint(res)

