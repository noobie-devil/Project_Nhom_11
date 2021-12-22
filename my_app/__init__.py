from flask import Flask, jsonify, request, render_template, Response, json, jsonify, redirect, url_for
import boto3
import botocore
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

app.config['AWS_CONFIGURE'] = {
    "aws_access_key_id": "ASIAUCYL4TURYEZFV7SV",
    "aws_secret_access_key": "0CdkuwyRKo8gh3RuJBJuPQDZTmCyCHoDgwbiKcX0",
    "aws_session_token": "FwoGZXIvYXdzED4aDEcQbvSAMBgaOUtsByLPAZfrKrT1NfyZXi4vQP8bBNGw2IduRXdQeGZ9EIoMlAMCyh8v6t97XbWqjDJLsRRH8Ouqb0jfWSO67XS+CsUGMGOO/bDlhubqFPnF3udNTp454PWfn7hTHTVuYpdUlbRp0vw/nId1t+9zqmEEzhYU7V+G/JtZ2JII5FES+ziMjlF7/zPQ/j8nTqmH9ZAgD7vFJUjELRIK1vl3fedVimFnjabp86BkiXVEuDgIjQOi9yIcQTSrhe1qtUn77h6lM/NlcPfvAXYol/sufDux0chyPij94YqOBjItyRH7Mw6D5WEjw8ItTdfjeS8OTt+zullo8ktu1NJnhXJCOgxUQX3CUODR04hm",
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


