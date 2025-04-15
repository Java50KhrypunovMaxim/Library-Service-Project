# 📚 Library Management API

A Django RESTful API for managing a library system. It allows authenticated users to borrow books and view their payments, while admins have full control over all data.

## 🚀 Features

- Book Management (Read-only for regular users)
- Borrowing System (borrow, view active/inactive borrowings)
- Payment System (automatic fine calculation, session handling)
- Admin Panel with custom display
- Pagination, Permissions & Filtering
- Token Authentication
- Swagger Documentation

## 🧠 Tech Stack

- Python 3.11+
- Django 4+
- Django REST Framework
- drf-spectacular (Swagger/OpenAPI)
- Token Authentication
- SQLite (or PostgreSQL)

## 🔐 Superuser Credentials

Used for accessing the Django Admin panel at `/admin/`

Email: Max170289@gmail.com  
Password: Max170289

## 🔧 Setup Instructions

1. Clone the repository  
   `git clone <your-repo-url>`  
   `cd <project-folder>`

2. Create & activate a virtual environment  
   `python -m venv env`  
   `source env/bin/activate`  (Windows: `env\Scripts\activate`)

3. Install dependencies  
   `pip install -r requirements.txt`

4. Apply migrations  
   `python manage.py migrate`

5. Run the development server  
   `python manage.py runserver`

## 🧪 API Endpoints

| Resource   | Endpoint                   | Methods       |
|------------|----------------------------|---------------|
| Books      | /api/library/books/        | GET           |
| Borrowings | /api/library/borrowings/   | GET, POST     |
| Payments   | /api/library/payments/     | GET           |
| Auth       | /api/user/token/           | POST          |
| Swagger UI | /api/doc/swagger/          | GET           |

## 📘 Admin Panel

Accessible at http://localhost:8000/admin/

Custom PaymentAdmin interface includes:
- Read-only session and payment fields
- Inline borrowing information

## 🔐 Authentication

Uses Token Authentication.

1. Obtain token:  
   `POST /api/user/token/`  
   Body:  
   ```json
   {
     "email": "your_email",
     "password": "your_password"
   }

