
# Xây dựng ứng dụng trên AWS cho phép tạo Database và cung cấp api để thêm, xóa, sửa trên Database

Đây là source code project cuối kì môn Điện toán đám mây của nhóm 11



## Các tính năng chính

- Thêm, xóa table DynamoDB
- Tương tác dữ liệu của table trực tiếp trên web
- Tương tác dữ liệu của table thông qua API được cung cấp


## Công nghệ sử dụng 

**Client:** Html, Css3, Bootstrap

**Server:** Flask Framework, AWS Lambda Function, AWS SQS

**Database:** DynamoDB


## Thành viên tham gia Project

- [@truongnguyenvan8801](https://github.com/truongnguyenvan8801) - 19110491@student.hcmute.edu.vn
- [@Vinh-san](https://github.com/Vinh-san) - 19110042@student.hcmute.edu.vn


## Yêu cầu 

Tạo 1 bảng để lưu thông tin người dùng với tên bảng là 'user_table', Partition Key là 'user_name' kiểu String, Sort Key là 'public_id' kiểu String

![App Screenshot](https://i.imgur.com/E8eQfCc.png)

Khởi tạo 1 Global secondary indexes trong bảng 'user_table' với Partition Key là 'email_address' với kiểu String

![App Screenshot](https://imgur.com/vrPluuO.png)

Tạo 1 bảng để lưu thông tin các bảng được tạo bởi người dùng với tên bảng là 'log_table', Partition Key là 'public_id' kiểu String, Sort Key là 'table_name' kiểu String

![App Screenshot](https://imgur.com/MWQwKCH.png)

Từ AWS Lambda Function, tạo 1 Lambda Function với đoạn code sau đây

```python3
import json
import boto3
import urllib
from urllib.parse import unquote
import re
import ast

def lambda_handler(event, context):
    # TODO implement
    data = event['Records'][0]['body']
    data = unquote(data)
    data = data.replace("\'", "\"")

    data = json.loads(data)
    

    response = create_dynamodb_table(data)
    print(response)
    

def create_dynamodb_table(event):
    AttributeDefinitions = [
    {
        'AttributeName': event['PartitionKey'],
        'AttributeType': event['PartitionKey_type']
    }
    ]
    KeySchema = [
    {
        'AttributeName': event['keyHash'],
        'KeyType': event['keyHash_type']
    }
    ]
    if event['SortKey'] != '':
        AttributeDefinitions.append({
            'AttributeName': event['SortKey'],
            'AttributeType': event['SortKey_type']
        })
        KeySchema.append({
            'AttributeName': event['keyRange'],
            'KeyType': event['keyRange_type']
        })
    try:
        client = boto3.resource('dynamodb')
        response = client.create_table(
            AttributeDefinitions = AttributeDefinitions,
            TableName=event['tablename'],
            KeySchema = KeySchema,
            BillingMode='PAY_PER_REQUEST',
        )
        response.meta.client.get_waiter('table_exists').wait(TableName=event['tablename'])
        return response
    except Exception as e: print(e)
```
Tạo 1 hàng đợi với AWS SQS dùng để trigger cho Function vừa tạo ở trên

![App Screenshot](https://imgur.com/avUTP9f.png)

Copy URL của hàng đợi vừa tạo ở trên, truy cập vào file routes.py và tìm đoạn code sau, thay giá trị của biến url thành đường dẫn của hàng đợi đã tạo ở trên

```bash
  vi Project_Nhom_11/my_app/routes.py
```
![App Screenshot](https://imgur.com/4c5XW4H.png)

Từ AWS Lambda Function, tạo 1 Lambda Function với đoạn code sau đây

```python3
import json
import boto3
import urllib
from urllib.parse import unquote
import re
import ast

def lambda_handler(event, context):
    # TODO implement
    # data = json.loads(event['Records'][0]['body']) 
    data = event['Records'][0]['body']
    data = unquote(data)
    data = data.replace("\'", "\"")

    data = json.loads(data)
    response = delete_dynamodb_table(data)
    print(response)

def delete_dynamodb_table(event):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(event['tablename'])
        response = table.delete()
        
        return response
    except Exception as e: print(e)
```
Tạo 1 hàng đợi với AWS SQS dùng để trigger cho Function vừa tạo ở trên

![App Screenshot](https://imgur.com/5rWih1l.png)

Copy URL của hàng đợi vừa tạo ở trên, truy cập vào file routes.py và tìm đoạn code sau, thay giá trị của biến url thành đường dẫn của hàng đợi đã tạo ở trên

```bash
  vi Project_Nhom_11/my_app/routes.py
```

![App Screenshot](https://imgur.com/WuWoKqo.png)


## Deploy lên AWS EC2

Để deploy project, thực hiện các lệnh sau

```bash
  sudo apt-get update
```
clone project về máy ảo
```bash
  git clone https://github.com/truongnguyenvan8801/Project_Nhom_11.git
```
Update các library cần thiết
```bash
  pip3 install --upgrade pip
```
```bash
  python3 -m pip install setuptools-rust
```
Truy cập vào thư mục chứa project
```bash
 cd Project_Nhom_11
```
Install các thư viện mà project yêu cầu
```bash
  python3 -m pip install -r requirements.txt
```
Truy cập file run.py
```bash
  vi run.py
```
Thay đổi từ 
```python3
    from my_app import app

    app.run(debug=True)
```
sang cấu hình phù hợp với máy ảo EC2
```python3
    from my_app import app

    app.run(host='0.0.0.0', port=8080)
```
Cung cấp các secret key cần thiết để sử dụng các tài nguyên trong AWS

```bash
  vi my_app/__init__.py
```
![App Screenshot](https://imgur.com/MJgWqhy.png)

Sau khi thực hiện các cấu hình cần thiết, để chạy chương trình thực hiện lệnh
```bash
  python3 run.py
```
