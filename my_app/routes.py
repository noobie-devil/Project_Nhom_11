from my_app import app, client, resource
from flask import Flask, flash, jsonify, request, render_template, Response, json, jsonify, redirect, url_for, make_response,session
import urllib3
import requests
from urllib.parse import quote
from my_app.forms import CreateTableForm
from boto3.dynamodb.conditions import Key
import botocore
from my_app.forms import *
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps



@app.route("/test")
def test():
    return render_template('test.html')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if session.get('access-token') is not None:
            token = session['access-token']

        if not token:
            
            return redirect(url_for('login_page'))

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            table = resource.Table('user_table')
            current_user = table.get_item(
                Key={
                    'user_name': data['user_name'],
                    'public_id': data['public_id']
                }
            )
        except:
            flash(f'Login session has expired!!! please login again.', category='danger')
            return redirect(url_for('login_page'))

        return f(current_user['Item'], *args, **kwargs)
    return decorated

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        public_id = str(uuid.uuid4())
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        response = create_user(user_name=form.username.data, public_id=public_id, email_address=form.email_address.data, password=hashed_password)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            flash(f'Account created successfully! Please log in.', category='success')
            return redirect(url_for('login_page'))
        flash(f'Error! An error occurred. Please try again later', category='danger')
        return render_template('register.html', form=form)
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        table = resource.Table('user_table')
        user = table.query(
            IndexName='email_address-index',
            KeyConditionExpression=Key('email_address').eq(form.email_address.data)
        )
        if user.get('Count') and check_password_hash(user.get('Items')[0]['password'], form.password.data):
            user = user.get('Items')[0]
            token = jwt.encode({
                'public_id': user['public_id'],
                'user_name': user['user_name'],
                'exp': datetime.utcnow() + timedelta(minutes=60)
            }, app.config['SECRET_KEY'])
            session['logged-in'] = True
            session['access-token'] = token
            session.permanent = True
            
            flash(f'Success! You are logged in as: {user["user_name"]}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    if session.get('logged-in') is not None and session.get('access-token') is not None:
        session['logged-in'] = False
        session.pop('access-token')
        flash("You have been logged out! ", category='info')
    return redirect(url_for("home_page"))

def create_user(user_name, public_id, email_address, password):
    table = resource.Table('user_table')
    response = table.put_item(
        Item={
            'user_name': user_name,
            'public_id': public_id,
            'email_address': email_address,
            'password': password,
            'is_admin': False
        }
    )
    return response

@app.route("/")
@app.route("/tables")
@token_required
def home_page(current_user):
    list_tables = get_tables(current_user)
    return render_template('index.html',tables=list_tables, current_user=current_user)

@app.route("/tables/ajax-get", methods=['GET'])
@token_required
def ajax_load_tables(current_user):

    return Response(
        json.dumps({'tables': get_tables(current_user)}),
        status=200,
        mimetype='application/json'
    )

def get_tables(current_user):
    public_id = current_user['public_id']
    get_tables = get_all_table_by_public_id(public_id)
    list_tables = []
    for table in get_tables:
        item = client.describe_table(TableName=str(table['table_name'] + '-' + public_id))
        item['Table']['TableName'] = item['Table']['TableName'].split('-' + public_id)[0]
        list_tables.append(item)

    return list_tables

@app.route("/tables/ajax-delete", methods=['POST'])
@token_required
def delete_tables(current_user):
    data = request.json
    url = 'https://sqs.us-east-1.amazonaws.com/280808430883/DeleteDynamoTableQueue'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    for table in data['tables']:

        payload = {
                "tablename": str(table + '-' + public_id)
        }
        payload = quote(str(payload))
        params = {
            'Action': 'SendMessage',
            'MessageBody': payload
        }
        send = requests.post(url, headers=headers, params=params)

    list_tables = get_tables(current_user)
    return Response(
        json.dumps({'tables': list_tables}),
        status=200,
        mimetype='application/json'
    )



@app.route('/items', methods=['POST'])
@token_required
def ajax_get_table(current_user):
    table_name = request.json['table_name']
    public_id = current_user['public_id']
    if table_name:
        table_name_origin = str(table_name + '-' + public_id)
        table = resource.Table(table_name_origin)
        response = table.scan()
        data = response['Items']
        columns = get_all_columns(table_name, public_id)
        return dict(html=render_template('load-data-table.html', table=data, columns=columns, table_name=table_name_origin))
    else:
        return Response(
            json.dumps({'error': 'invalid'}),
            status=400,
            mimetype='application/json'
        )
    
@app.route('/items')
@token_required
def items_page(current_user):
    list_tables = get_all_table_by_public_id(current_user['public_id'])
    return render_template('items.html', list_tables=list_tables)

@app.route("/edit-item")
@token_required
def edit_item_page(current_user):
    table_name_origin = request.args.get('table-name')
    public_id = current_user['public_id']
    table_name = table_name_origin.split('-' + public_id)[0]
    all_columns = get_all_columns(table_name,public_id)
    data = client.describe_table(TableName=table_name_origin)
    data = data['Table']
    list_key = []
    for keySchema in data['KeySchema']:
        for attr in reversed(data['AttributeDefinitions']):
            if keySchema['AttributeName'] == attr['AttributeName']:
                key = {}
                key['AttributeName'] = keySchema['AttributeName']
                key['AttributeType'] = attr['AttributeType']
                list_key.append(key)
                break

    return render_template('edit-item.html',table_name=table_name, data=data, list_key=list_key, all_columns=all_columns)  

@app.route("/edit-item/ajax-edit-item", methods=['POST'])
@token_required
def ajax_edit_item(current_user):
    data = request.json
    public_id = current_user['public_id']
    table_name = str(data['table_name'] + '-' + public_id)
    existing_tables = client.list_tables()['TableNames']
    # Get all columns current in table target
    all_columns_current = get_all_columns(data['table_name'], public_id)
    new_cols = []
    for attribute,value in data['data'].items():
        if attribute not in all_columns_current:   
            new_cols.append(attribute)

    if table_name in existing_tables:
        table = resource.Table(table_name)
        if request.method == 'POST' or request.method == 'PUT':
            try:
                response = table.put_item(Item=data['data'])
                # check if user input new attibute to table
                if len(new_cols) > 0:
                    append = append_new_col_to_table(new_cols, data['table_name'], public_id)
                # if append return true, success add new col to log table
                if append:
                    return Response(
                        json.dumps({'response': response}),
                        status=200,
                        mimetype='application/json'
                    )
            except botocore.exceptions.ClientError as err:

                return Response(
                    json.dumps({'Error Message': err.response['Error']['Message']}),
                    status=err.response['ResponseMetadata']['HTTPStatusCode'],
                    mimetype='application/json'
                )
        else:
            return Response(
                json.dumps({"Error Message": "bad request."}),
                status=400,
                mimetype='application/json'
            ) 
    else:
        return Response(
            json.dumps({"Error Message": "table not existings."}),
            status=400,
            mimetype='application/json'
        )



@app.route("/tables/<table_name>/", methods=['DELETE'])
def api_delte(table_name):
    existing_tables = client.list_tables()['TableNames']
    if table_name in existing_tables:
        table = resource.Table(table_name)
        if request.method == 'DELETE':
            params = request.json
            try:
                response = table.delete_item(Key=params)
                return Response(
                    json.dumps({'response': response}),
                    status=200,
                    mimetype='application/json'
                )
            except botocore.exceptions.ClientError as err:

                return Response(
                    json.dumps({'Error Message': err.response['Error']['Message']}),
                    status=err.response['ResponseMetadata']['HTTPStatusCode'],
                    mimetype='application/json'
                )
        else:
            return Response(
                json.dumps({"Error Message": "bad request."}),
                status=400,
                mimetype='application/json'
            ) 
    else:
        return Response(
            json.dumps({"Error Message": "table not existings."}),
            status=400,
            mimetype='application/json'
        )    

def append_new_col_to_table(new_cols, table_name, public_id):
    table = resource.Table('log_table')
    result = table.update_item(
        TableName='log_table',
        Key={
            'public_id': public_id,
            'table_name': table_name
        },
        UpdateExpression='SET #attr= list_append(if_not_exists(#attr, :empty_list), :my_value)',
        ExpressionAttributeValues={
            ":my_value": new_cols,
            ":empty_list": []
        },
        ExpressionAttributeNames={
            "#attr": 'columns',
        },
        ReturnValues='UPDATED_NEW'
    )
    if result['ResponseMetadata']['HTTPStatusCode'] == 200 and 'Attributes' in result:
        return True
    else:
        return False

# @app.route("/tables/category_table/append", methods=['POST'])
# def append_list():
#     data = request.json
#     table = resource.Table('category_table')
#     result = table.update_item(
#         TableName='category_table',
#         Key={
#             'category_id': 1231,
#             'category_name': 'user_1'
#         },
#         UpdateExpression='SET #attr= list_append(if_not_exists(#attr, :empty_list),:my_value)', #'SET #col = list_append(if_not_exists(#col, :empty_list), :my_value)',
#         ExpressionAttributeValues={
            
#             ":my_value": ["alo_men"], 
#             ":empty_list": []
            
#         },
#         ExpressionAttributeNames={
#         "#attr": "Columns",

#         },
#         ReturnValues="UPDATED_NEW"
#     )
#     if result['ResponseMetadata']['HTTPStatusCode'] == 200 and 'Attributes' in result:
#         return Response(
#             json.dumps({'data': result['Attributes']['Columns']}),
#             status=200,
#             mimetype='application/json'
#         ) 

@app.route("/tables/<table_name>/", methods=['PUT', 'POST'])
def api_update(table_name):
    existing_tables = client.list_tables()['TableNames']
    if table_name in existing_tables:
        table = resource.Table(table_name)
        if request.method == 'POST' or request.method == 'PUT':
            params = request.json
            try:
                response = table.put_item(Item=params)
                return Response(
                    json.dumps({'response': response}),
                    status=200,
                    mimetype='application/json'
                )
            except botocore.exceptions.ClientError as err:

                return Response(
                    json.dumps({'Error Message': err.response['Error']['Message']}),
                    status=err.response['ResponseMetadata']['HTTPStatusCode'],
                    mimetype='application/json'
                )
        else:
            return Response(
                json.dumps({"Error Message": "bad request."}),
                status=400,
                mimetype='application/json'
            ) 
    else:
        return Response(
            json.dumps({"Error Message": "table not existings."}),
            status=400,
            mimetype='application/json'
        )
        


def get_all_table_by_public_id(public_id=None):
	query = query_table(table_name='log_table',key='public_id',value=public_id)
	return query.get('Items')
   


def get_all_columns(table_name, public_id):
    table = resource.Table('log_table')
    response = table.get_item(
        Key = {
            'public_id': public_id,
            'table_name': table_name
        }
    )
    return response['Item']['columns']

@app.route("/create-tables", methods=["POST", "GET"])
@token_required
def create_tables_page(current_user):
    form = CreateTableForm()
    
    if request.method == "POST":
        table_name = request.form.get('table_name') + '-' + current_user['public_id']
        existing_tables = client.list_tables()['TableNames']
        if table_name not in existing_tables:
            partition_key = request.form.get('partition_key')
            sort_key = request.form.get('sort_key')
            columns = []

            columns.append(partition_key)
            if sort_key != None:
                columns.append(sort_key)

            log_table = resource.Table('log_table')
            response = log_table.put_item(
                Item={
                    'public_id': current_user['public_id'],
                    'table_name': request.form.get('table_name'),
                    'columns': columns
                }
            )

            url = "https://sqs.us-east-1.amazonaws.com/280808430883/CreateDynamoTableQueue"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            
            payload = {
                "tablename": table_name,
                "keyHash": partition_key,
                "keyHash_type": "HASH",
                "PartitionKey": partition_key,
                "PartitionKey_type": request.form.get('partition_key_type'),
                "keyRange": sort_key,
                "keyRange_type": "RANGE",
                "SortKey": sort_key,
                "SortKey_type": request.form.get('sort_key_type')
            }
            payload = quote(str(payload))
            params = {
                'Action': 'SendMessage',
                'MessageBody': payload
            }
            
            send = requests.post(url, headers=headers, params=params)

            
            return redirect(url_for('home_page'))
            
        else:
            flash(f'A table with the same name already exists. Table names in the same account and same AWS Regions must be unique.', category='danger')
        
    return render_template('create-tables.html', form=form)    
