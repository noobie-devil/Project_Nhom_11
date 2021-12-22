from flask import Flask, jsonify, request, render_template, Response, json, jsonify, redirect, url_for
import boto3
import botocore
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

app.config['AWS_CONFIGURE'] = {
    "aws_access_key_id": "ASIAUCYL4TURQWJM3KEE",
    "aws_secret_access_key": "5Aqy3hJepd/Vx1WBpUdIBl3om+qYGfZ5SEdCBPqr",
    "aws_session_token": "FwoGZXIvYXdzEEQaDBVxQVRouwv5vfEn3yLPAW3ty2zR5qVEAqNBd5tVZX5GD6312Ij0dxDSMrOwEmHhoCOfSotQxCWrfbyCoGjcv6qckXTfoePIpM9hqYX5k4hrd9bo8kNlj+covGVW2Ob0dPgfYW4r9aACqhxTMe3TfOrm3o7/ocRnDLGLVkwRBKGlBMkJ5gDPPlFuXvzJNFzK7S6JzPEmdzJvurWHm3DZzTU8ImnZEiG79x9TvR4VGKZIh9WGYN2pme0XNa9XkIeG9XBlT8yhTmW/JTN3060CXmMnUo/76HuvO7wfcnNGtii/h4yOBjItTi/5WdfpGLkH4YvmPMMbR2jCB/3yxsjXf4/3u2yjT3Gutm29Xv0VaNnpgDko",
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


