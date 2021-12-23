from flask import Flask, jsonify, request, render_template, Response, json, jsonify, redirect, url_for
import boto3
import botocore
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

app.config['AWS_CONFIGURE'] = {
    "aws_access_key_id": "ASIAUCYL4TUR5SFZRDLB",
    "aws_secret_access_key": "AUvw+EnIbv/A+o0URwn3a9SmPX0LsA3M7IjrmeZf",
    "aws_session_token": "FwoGZXIvYXdzEF8aDGzN9QRdedckOX9FwiLPAS4Xqd06/PBzPJ07VoukThLCaf3FhAf5cs9JMvypInrxhCuAuxsHmi5EXFNBrTHxm+kdVazjxwxZwyzbikQuawP7THHlhBJNZpAV0W23Q5Evf5rqpFdrN7U9oad++TX/83PR67SAHuiaGoyO0PXfZqJ/+3a1gbSUTvSUWvjlCvSO/yTBxcmsunkXVQQ1SzAi/H9NxbDtiF+RKkkOLRHGfGCkg2dxvlYHNYl5P+nU+JlYYY/wDEV2vRaEgwc4gm2sdMfwLj+Zm0OPHA92MSewqSiJ+pGOBjItTe1sHhI6fXOUMZafRFeUl5s/eXq7ZYahp5+SXMY4wffnVvWcOvBEeWz8xr0n",
    'region_name': 'us-east-1'
}


client = boto3.client('dynamodb',aws_access_key_id=app.config["AWS_CONFIGURE"]["aws_access_key_id"], 
    aws_secret_access_key=app.config["AWS_CONFIGURE"]["aws_secret_access_key"], 
    aws_session_token=app.config["AWS_CONFIGURE"]["aws_session_token"], 
    region_name=app.config["AWS_CONFIGURE"]["region_name"]
)
resource = boto3.resource('dynamodb',aws_access_key_id=app.config["AWS_CONFIGURE"]["aws_access_key_id"], 
    aws_secret_access_key=app.config["AWS_CONFIGURE"]["aws_secret_access_key"], 
    aws_session_token=app.config["AWS_CONFIGURE"]["aws_session_token"], 
    region_name=app.config["AWS_CONFIGURE"]["region_name"]
)


from my_app import routes
from my_app import api
from my_app import admin


