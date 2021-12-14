from flask import Flask, jsonify, request, render_template, Response, json, jsonify, redirect, url_for
import boto3
import botocore
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

app.config['AWS_CONFIGURE'] = {
    "aws_access_key_id": "ASIAUCYL4TUR4AITQHWK",
    "aws_secret_access_key": "7oA95AimT0EVxqtDZSKsVEwZPUoA4qGVAK8oH9Ja",
    "aws_session_token": "FwoGZXIvYXdzEIb//////////wEaDA8jOiQm3HI7Rr+H5SLPAStUu2ecYk1heHNGxCvr8mv36b2/IJ3rUs9vIJxrOXXnAbFElBRe2XhCwsirJzvlidIyZPk/MEM2dialVqXcmgqeZEpWFommHDVrvfhIZZ9V8GxZe5jpyHHztqzeqOLRwwx+hCWvgMDlz6fKxiePFGJTCqG2ErSGdKPIQnAtFdX3/w9z+2VcXC2aBhsa74CVyU3a3/7xavyRgIAI7tN7B06f/uLvebhtV2jwXdMnAdlfq2tzM6yYv3QntW0J5ctwWZ/b8px5YpAVN1eJnt4T5iien+KNBjItPZxmzCgFAjjlgIEotGiM9TgSRNFHc/ZTKzvVA2eZqCUciHwLItNrK3cEVdU/",
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
