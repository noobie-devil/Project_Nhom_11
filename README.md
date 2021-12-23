
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


## Yêu cầu trước khi deploy project

Tạo 1 bảng để lưu thông tin người dùng với tên bảng là 'user_table', Partition Key là 'user_name' kiểu String, Sort Key là 'public_id' kiểu String

![App Screenshot](https://i.imgur.com/E8eQfCc.png)

Khởi tạo 1 Global secondary indexes trong bảng 'user_table' với Partition Key là 'email_address' với kiểu String

![App Screenshot](https://imgur.com/vrPluuO.png)

Tạo 1 bảng để lưu thông tin các bảng được tạo bởi người dùng với tên bảng là 'log_table', Partition Key là 'public_id' kiểu String, Sort Key là 'table_name' kiểu String

![App Screenshot](https://imgur.com/MWQwKCH.png)


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
