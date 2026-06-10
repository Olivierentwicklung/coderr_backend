# 🚀 Coderr API

![Django](https://img.shields.io/badge/Django-5.x-green)
![DRF](https://img.shields.io/badge/DRF-3.x-blue)
![Auth](https://img.shields.io/badge/Auth-Token-orange)
![Status](https://img.shields.io/badge/Project-Active-brightgreen)

A modern freelance marketplace backend built with Django REST Framework.

Coderr enables customers to purchase services from business users, manage orders, leave reviews, and maintain professional profiles through a clean RESTful API architecture.

---

## 🚀 Features

- 🔐 User registration and authentication
- 👤 Customer and business user profiles
- 📦 Service offers with multiple package tiers
- 📁 File upload support
- 🛒 Order management system
- ⭐ Review and rating system
- 📊 Business user statistics
- 🔍 Public profile discovery
- ⚙️ RESTful API powered by Django REST Framework

---

## 📦 Setup

### Requirements

- Python 3.12+
- pip / virtualenv
- SQLite (default)
- Pytest + Coverage
- Optional: Postman

---

### Local Installation

```bash
git clone https://github.com/Olivierentwicklung/coderr_backend.git

cd coderr-backend

python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

cp .env.template .env
     - Open the new .env file and replace the placeholders with your actual local secrets.

python manage.py migrate

pytest

python manage.py runserver
```

---

## 🧪 Example Usage

### Open Django Administration

```text
http://127.0.0.1:8000/admin/
```

### Open coderr API Endpoint Dokumentation

```text
http://127.0.0.1:8000/api/schema/swagger-ui/
```

---

## 🔐 Authentication Endpoints

| Method | Endpoint             | Description             |
| ------ | -------------------- | ----------------------- |
| POST   | `/api/registration/` | Register a new user     |
| POST   | `/api/login/`        | Login and receive token |

### Authentication Header

Authenticated requests require:

```http
Authorization: Token <your_token>
```

---

## 👤 Profile Endpoints

| Method | Endpoint                  | Description            |
| ------ | ------------------------- | ---------------------- |
| GET    | `/api/profile/{id}/`      | Retrieve user profile  |
| PATCH  | `/api/profile/{id}/`      | Update user profile    |
| GET    | `/api/profiles/business/` | List business profiles |
| GET    | `/api/profiles/customer/` | List customer profiles |

---

## 📦 Offer Endpoints

| Method | Endpoint                  | Description            |
| ------ | ------------------------- | ---------------------- |
| GET    | `/api/offers/`            | List offers            |
| POST   | `/api/offers/`            | Create offer           |
| GET    | `/api/offers/{id}/`       | Retrieve offer         |
| PATCH  | `/api/offers/{id}/`       | Update offer           |
| DELETE | `/api/offers/{id}/`       | Delete offer           |
| GET    | `/api/offerdetails/{id}/` | Retrieve offer details |

---

## 🛒 Order Endpoints

| Method | Endpoint                                         | Description      |
| ------ | ------------------------------------------------ | ---------------- |
| GET    | `/api/orders/`                                   | List orders      |
| POST   | `/api/orders/`                                   | Create order     |
| PATCH  | `/api/orders/{id}/`                              | Update order     |
| DELETE | `/api/orders/{id}/`                              | Delete order     |
| GET    | `/api/order-count/{business_user_id}/`           | Total orders     |
| GET    | `/api/completed-order-count/{business_user_id}/` | Completed orders |

---

## ⭐ Review Endpoints

| Method | Endpoint             | Description   |
| ------ | -------------------- | ------------- |
| GET    | `/api/reviews/`      | List reviews  |
| POST   | `/api/reviews/`      | Create review |
| PATCH  | `/api/reviews/{id}/` | Update review |
| DELETE | `/api/reviews/{id}/` | Delete review |

---

## Base-info Endpoints

| Method | Endpoint          | Description           |
| ------ | ----------------- | --------------------- |
| GET    | `/api/base-info/` | List base information |

---

## 🧾 Example Requests

### Register User

```json
{
  "username": "exampleUsername",
  "email": "example@mail.de",
  "password": "examplePassword",
  "repeated_password": "examplePassword",
  "type": "customer"
}
```

### Create Review

```json
{
  "business_user": 2,
  "rating": 5,
  "description": "Excellent service and communication."
}
```

---

## 🗂️ Project Structure

```text
coderr_backend/
├── manage.py
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── base_info_app/
│   ├── views.py
│   └── urls.py
│
├── users_auth_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── uploads_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── offers_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── orders_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── reviews_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── tests/
│   ├── base_info_app/
│   ├── users_auth_app/
│   ├── uploads_app/
│   ├── offers_app/
│   ├── orders_app/
│   └── reviews_app/
│
├── requirements.txt
└── pytest.ini
```

---

## 🧠 ERD Overview

### Core Entities

- CustomUser
- FileUpload
- Offer
- OfferDetail
- OfferDetailFeature
- Order
- Review

### Relationships

```text
Abstract_user 1 ─── 1 CustomUser

CustomUser 1 ─── many Offer
as business_user

Offer 1 ─── 3 OfferDetail

OfferDetail 1 ─── many OfferDetailFeature

CustomUser 1 ─── many Order
as customer

OfferDetail 1 ─── many Order

CustomUser 1 ─── many Review
as reviewer

CustomUser 1 ─── many Review
as reviewed business_user

FileUpload 1 ─── M CustomUser

FileUpload 1 ─── M Offer
```

---

# 🎥 Demo

## ERD

![ERD](z_screenshots/erd.drawio.png)

## Django Admin

![Admin](z_screenshots/admin_panel.png)

## API Testing

![Tests](z_screenshots/tests_results.png)

---

## 🔒 Security

- Token-based authentication
- Protected API endpoints
- Ownership-based permissions
- User role separation
- Serializer validation
- Secure file uploads

---

## 🧑‍💻 Tech Stack

- Python
- Django
- Django REST Framework
- DRF Token Authentication
- SQLite
- Pytest
- Coverage
- Postman

---

## ✨ Purpose

Coderr was developed as a freelance marketplace backend project to practice and demonstrate:

- Django REST Framework architecture
- Custom authentication systems
- Relational database design
- RESTful API development
- Business logic implementation
- File upload management
- Testing with Pytest
- Clean project organization
- Real-world marketplace workflows
