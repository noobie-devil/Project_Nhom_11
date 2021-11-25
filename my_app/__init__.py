# app.py

# import os

# import boto3

from flask import Flask, jsonify, request, render_template, make_response
import urllib3
import requests
from urllib.parse import quote
from my_app.forms import CreateTableForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'

# USERS_TABLE = os.environ['USERS_TABLE']
# IS_OFFLINE = os.environ.get('IS_OFFLINE')


# if IS_OFFLINE:
#     client = boto3.client(
#         'dynamodb',
#         region_name='localhost',
#         endpoint_url='http://localhost:8000'
#     )
    
# else:
#     client = boto3.client('dynamodb')


@app.route("/")
@app.route("/tables")
def home_page():
    return render_template('index.html')

@app.route("/create-tables", methods=["POST", "GET"])
def create_tables_page():
    form = CreateTableForm()
    
# #     {
# #   "tablename": "user_table",
# #   "keyHash": "user_id",
# #   "keyHash_type": "HASH",
# #   "PartitionKey": "user_id",
# #   "PartitionKey_type": "N",
# #   "keyRange": "username",
# #   "keyRange_type": "RANGE",
# #   "SortKey": "username",
# #   "SortKey_type": "S"
# # }
    if request.method == "POST":
        # req = request.get_json(force=True)
        # # # req = json.dumps(req)
        # # # data = json.loads(req)

        # # # print(data['MessageBody'])
        # print(str(req['MessageBody']))
        # res = make_response(jsonify(req['MessageBody']), 200)
        # return res
        # req = request.get_json()
        # print(req)
        # return make_response(jsonify(req),200)
        url = "https://sqs.us-east-1.amazonaws.com/280808430883/CreateDynamoTableQueue"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        payload = {
            "tablename": request.form.get('table_name'),
            "keyHash": request.form.get('partition_key'),
            "keyHash_type": "HASH",
            "PartitionKey": request.form.get('partition_key'),
            "PartitionKey_type": request.form.get('partition_key_type'),
            "keyRange": request.form.get('sort_key'),
            "keyRange_type": "RANGE",
            "SortKey": request.form.get('sort_key'),
            "SortKey_type": request.form.get('sort_key_type')
        }
        payload = quote(str(payload))
        params = {
            'Action': 'SendMessage',
            'MessageBody': payload
        }
        # response = app.response_class(
        #     response=json.dumps(payload),
        #     mimetype='application/json'
        # )
        send = requests.post(url, headers=headers, params=params)
        # response = app.response_class(
        #     response=json.dumps(send.status_code),
        #     mimetype='application/json'
        # )
        print(send.url)
        return app.response_class(
            send.text,
            status=send.status_code,
            content_type=send.headers['content-type'],
        )
        return response
        # return jsonify(payload)
#         purchased_item = request.form.get('purchased_item')
#         p_item_object = Item.query.filter_by(name=purchased_item).first()
#     payload = {'some': 'data'}
    return render_template('create-tables.html', form=form)    

# @app.route("/users/<string:user_id>")

# def get_user(user_id):
#     resp = client.get_item(
#         TableName=USERS_TABLE,
#         Key={
#             'userId': { 'S': user_id }
#         }
#     )

#     item = resp.get('Item')
#     if not item:
#         return jsonify({'error': 'User does not exist'}), 404

#     return jsonify({

#         'userId': item.get('userId').get('S'),

#         'name': item.get('name').get('S')

#     })



# @app.route("/users", methods=["POST"])

# def create_user():

#     user_id = request.json.get('userId')

#     name = request.json.get('name')

#     if not user_id or not name:

#         return jsonify({'error': 'Please provide userId and name'}), 400


#     resp = client.put_item(

#         TableName=USERS_TABLE,

#         Item={

#             'userId': {'S': user_id },

#             'name': {'S': name }

#         }

#     )


#     return jsonify({

#         'userId': user_id,

#         'name': name

#     })