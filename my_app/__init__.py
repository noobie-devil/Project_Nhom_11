from flask import Flask, jsonify, request, render_template, Response, json, jsonify, redirect, url_for
import boto3
import botocore
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

app.config['AWS_CONFIGURE'] = {
    "aws_access_key_id": "ASIAUCYL4TURS7P223GX",
    "aws_secret_access_key": "3mxHgN+AqSfG+8O5uI7J5QVj7pvkUz2Q+lVfGqZp",
    "aws_session_token": "FwoGZXIvYXdzEIL//////////wEaDOwe/fUdex1BYZZCQSLPAV/vLoyGBCM+JcQmWnjEpgZHI7AGlBfCawyKc0BtqjFXUHe0rQ/InmbME+6EcRZrlzQShDCP2tDITZI5mwTt+4rkbaoZu6lVqAy7J24a4pQWrtfaHV0DCRoanxY0c5lP9jCxbuNqSr9zwjzYPg/5ZXHFFt6A51VOqodewORFqayxnzcdp5SYBpoSFa0oIKMXf2yXZqcXVwhPF8nTue1U2/5+v3jK4mcg7WK2hBTRHgfvKyBv7RCcUN1UHt9c8fFf2Pl2GNx25tFgBM+rSQ32Pii7q+GNBjItTgEoobc9rC0+Z/+iFdyOA2IC0JljCVxWScXBCyT391in2gxu3Lyd5ScKhsz/",
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
