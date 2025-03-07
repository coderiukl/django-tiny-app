# 📌 Project: Todo-List

## 📑 MỤC LỤC
1. [Thông tin thành viên](#👥-thông-tin-thành-viên)
2. [Giới thiệu](#📖-giới-thiệu)
3. [Hướng dẫn cài đặt và chạy ứng dụng](#🚀-hướng-dẫn-cài-đặt-và-chạy-ứng-dụng)
   - [Clone repository](#1️⃣-clone-repository)
   - [Di chuyển vào thư mục dự án](#2️⃣-di-chuyển-vào-thư-mục-dự-án)
   - [Tạo môi trường ảo](#3️⃣-tạo-môi-trường-ảo-venv)
   - [Kích hoạt môi trường ảo](#4️⃣-kích-hoạt-môi-trường-ảo)
   - [Cài đặt dependencies](#5️⃣-cài-đặt-dependencies)
   - [Thiết lập database](#6️⃣-thiết-lập-database)
   - [Chạy ứng dụng](#7️⃣-chạy-ứng-dụng)
4. [Công nghệ sử dụng](#📌-công-nghệ-sử-dụng)


---

## 👥 Thông tin thành viên
- **Nguyễn Hữu Phúc** - `22676511`
- **Trần Trọng Trí** - `22665961`

---

## 📖 Giới thiệu
**Todo-List** là một ứng dụng web đơn giản giúp bạn quản lý công việc hàng ngày. Người dùng có thể tạo danh sách việc cần làm, chỉnh sửa, đánh dấu hoàn thành hoặc xóa công việc.

---

## 🚀 Hướng dẫn cài đặt và chạy ứng dụng

## 🚀 Cách 1:

### 1️⃣ **Clone repository**
Mở terminal hoặc command prompt và chạy lệnh:
```sh
 git clone https://github.com/coderiukl/django-tiny-app.git
```

### 2️⃣ **Di chuyển vào thư mục dự án**
```sh
 cd todo_project
```

### 3️⃣ **Tạo môi trường ảo (`venv`)**
```sh
 python -m venv venv
```

### 4️⃣ **Kích hoạt môi trường ảo**
- **Windows:**
  ```sh
  ./venv/Scripts/Activate.ps1
  ```
- **Mac/Linux:**
  ```sh
  source venv/bin/activate
  ```

### 5️⃣ **Cài đặt dependencies**
```sh
 pip install -r requirements.txt
```

### 6️⃣ **Thiết lập database**
```sh
 python manage.py makemigrations
 python manage.py migrate
```

### 7️⃣ **Chạy ứng dụng**
```sh
 python manage.py runserver
```

Sau đó, mở trình duyệt và truy cập **[http://127.0.0.1:8000](http://127.0.0.1:8000)** để sử dụng ứng dụng.

## 🚀 Cách 2: Chạy trên Docker

### 1️⃣ **Clone repository**
Mở terminal hoặc command prompt và chạy lệnh:
```sh
 git clone https://github.com/coderiukl/django-tiny-app.git
```
### 2️⃣ **Di chuyển vào thư mục dự án**
```sh
 cd todo_project
```
### 3️⃣ **Đóng gói**
Mở terminal hoặc command prompt và chạy lệnh, bước này sẽ khởi tạo images:
```sh
 docker-compose build 
```
Sau đó chạy lệnh:
```sh
 docker-compose up
```
Để khởi tạo container.
### 4️⃣ **Vào container bằng cách**
```sh
 docker ps
 docker exec -it <container_id> bash
 python manage.py makemigrations
 python manage.py migrate
```
### 5️⃣ **Chạy ứng dụng**
Nhấn chuột vào ports 8000:8000

![image](https://github.com/user-attachments/assets/1c65f73f-e395-421f-a58e-dc791c7fd0d6)

![image](https://github.com/user-attachments/assets/9b6790ce-808c-4f69-ac5d-5304e4b6deb7)

---

## 📌 Công nghệ sử dụng
- **Python** (Django)
- **HTML, CSS, JavaScript**
- **PostgresSQL** (Database)

---

