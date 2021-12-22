from flask import Flask, jsonify, request, render_template, Response, json, jsonify, redirect, url_for
import boto3
import botocore
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

app.config['AWS_CONFIGURE'] = {
    "aws_access_key_id": "ASIAUCYL4TUR44KDIGF4",
    "aws_secret_access_key": "tX1vO14TrHbbPo1k7ltVZdoIwLFsahVHBA/dcJO2",
    "aws_session_token": "FwoGZXIvYXdzEDAaDMWA1uKF8z47bc/wmiLPAWUTmxqC4gC0oJ7s58XjtXOl8NNVuLCkS7OoCXnPosYXV0aBECpD79cQyXwposcRCPuQqMGbUMSSVfUtZ4UPuxHb5lorsY8jXZ+a9zuxbOhiMMov3acpVbIV1Qu58yjHI0IHJ8nqj6FkufR9iToH0LnCBmIcNiulHvjaHMpuD88XQtQViKfA+iHRZAC5fhDeGzMFU16HGotePKjRTYjfsH8u71orDOCAinBqE1duAcvcoLVxb8waynuWrX3hS8ey7+P3NbEIIJ4IOzHbRePQrijPy4eOBjItgHU9plYqgePIpwTXmVnAQLXM0T2UDk98xLLcxC9tS738nP9oBdBe3ENnNKde",
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


