from flask import Flask, jsonify, request, render_template, make_response
import urllib3
import requests
from urllib.parse import quote
from my_app.forms import CreateTableForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'



@app.route("/")
@app.route("/tables")
def home_page():
    return render_template('index.html')

@app.route("/create-tables", methods=["POST", "GET"])
def create_tables_page():
    form = CreateTableForm()

    if request.method == "POST":
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
        
        send = requests.post(url, headers=headers, params=params)
        
        print(send.url)
        return app.response_class(
            send.text,
            status=send.status_code,
            content_type=send.headers['content-type'],
        )
        return response
        
    return render_template('create-tables.html', form=form)    
