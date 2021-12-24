from flask import Flask, jsonify, request, render_template, Response, json, jsonify, redirect, url_for
import boto3
import botocore
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

app.config['AWS_CONFIGURE'] = {
    "aws_access_key_id": "ASIAUCYL4TURVCXBRB2E",
    "aws_secret_access_key": "RQTX6i332v8VepyJf1RJLsDX6eCU1TH4385iPwtx",
    "aws_session_token": "FwoGZXIvYXdzEG4aDCvjmm4Uo+1fx9NQlCLPAUHGwCLlBPuB1tXvTx9WUxK8IInwq2HLjCMZyogwXutGj3yqBwqSyROcz7LyZ9tQB4LVcQZvpwgPPEbjqlTIcr0/fGgTJXPjG6BHrdUaR8UXg0tpkHKQ6xFzsJoQbmZF6WYodaoiTZ+s3H3MSMUsfQ2wVAq5EReGJLGhj8F1uJkKuBpVJnZaix7xYGu3q69l0rR4d68SUhmsWr5LSN+PXQ4FIL06HGXtxATNYA6E7x3FNsiyS+7Z6mbO4GgSsSgC9lJo2/plvFfod1Cs1tos9CjzpZWOBjItZ8+LrG0b6tE0tiSfrL2MGW2KEvk7IzHKnlAmekyGL2j+mY74Vm4+sjrPdIep",
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


