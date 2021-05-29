import os, sys
import re
import boto3
from botocore.config import Config
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import uuid
from datetime import date, datetime, timezone, timedelta
import time
import random
import json

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

# get articles from blog

path = "/home/ec2-user/environment/blog/content/aws"
dirs = os.listdir( path )

tiexp = 'title = "(.+?)"'
tgexp = 'tags = \[(.+?)\]'
dtexp = 'date = "(.+?)"'
coexp = '\n[+]{3}\n(.*)'

articles = []

for filename in dirs:
    fpt = os.path.join(path, filename)
    fop = open(fpt, 'r')
    fco = fop.read()
    
    mat = re.search(tiexp, fco)
    if mat:
        title = mat.group(1)
        
    mat = re.search(tgexp, fco)
    if mat:
        found = mat.group(1)
        tags = [stg.replace('"', '').strip() for stg in found.split(',')]
        
    mat = re.search(dtexp, fco)
    if mat:
        found = mat.group(1)
        dte = datetime.fromisoformat(found)
    
    mat = re.search(coexp, fco, flags=re.DOTALL)
    if mat:
        fco = mat.group(1)
    
    articles.append({
        "content": fco,
        "title": title,
        "category": '',
        "tags": tags,
        "date": int(dte.timestamp() * 1000),
        "lank": 0
    })
    
    
for article in articles:
    res = es.index(
        index=INDEX, 
        id=str(uuid.uuid1()), 
        body=json.dumps(article), 
        doc_type=TYPE
    )
    print(res)



