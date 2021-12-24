from flask import Flask, jsonify, request, render_template, Response, json, jsonify, redirect, url_for
import boto3
import botocore
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

app.config['AWS_CONFIGURE'] = {
    "aws_access_key_id": "ASIAUCYL4TURQG5XO3CY",
    "aws_secret_access_key": "OvFmR5j1E5j6h0fcDnW1xO4D2VQnn50pJseQUUT7",
    "aws_session_token": "FwoGZXIvYXdzEHIaDC2b3ACOkdyl2zM+cCLPAXXTjYiUEMFW58LwmPsQdj4EKFmw/6CR7to9Y5vuqyVFd/enBE847tNTKfSR0Im9G6qhM7OruS7dW3eFEm+Ngl1QkDR4YCMrRckHTXftb/LFfXtKkzIEkVPl29DqTFAIEGuN/mFp97MLZTQU+HZkb9KkjISzMR9FfQrvre4JdtqqMTXgUMNVvp8r6e/ob3YIjsnzPapaQ01qYN1wFF2yOqm/od2J3ppqT/hsjHQbTLeLWhe9kTngz2H9OxHgoa4yYAnumokuYAf5bN0aA6JcQCjylpaOBjItlzssBKDCcsnwrxIgB8ZIE7hIRRyWsWHbMzKQZOtyJ50V0apQaF4M7kg+cxG2",
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
from my_app import first_init

