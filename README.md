# Klyo Backend

A production-style e-commerce backend built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.  
This project demonstrates clean backend architecture, secure JWT authentication, role-based access control (RBAC), inventory handling, and a complete order lifecycle.

## Features

### Authentication & User Management
- User registration
- JWT-based login
- OAuth2 password flow
- Password hashing
- Role-based authorization (`admin`, `customer`)
- Retrieve the current user profile
- Admin-only user management

### Category Management
- Create categories
- Update categories
- Soft delete categories
- Auto-generate slugs
- Duplicate name/slug protection
- Active/inactive category support
- Admin-only full category listing
- Category detail view with nested product list

### Product Management
- Create products
- Update products
- Soft delete products
- Product listing with:
  - Pagination
  - Sorting
  - Search
  - Price filtering
  - Category filtering
  - Active/inactive filtering
- Prevent product creation or update under inactive categories
- Hide products from inactive categories by default
- Optional admin visibility for products under inactive categories

### Order Management
- Create orders
- Multi-item order support
- Stock validation before order creation
- Automatic stock deduction
- View a customer’s own orders
- Admin view of all orders
- Cancel orders with stock restoration
- Order status management
- Admin-only order status updates
- Supported statuses:
  - `pending`
  - `shipped`
  - `delivered`
  - `cancelled`

## Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy ORM**
- **Pydantic**
- **JWT Authentication**
- **OAuth2PasswordBearer**
- **Passlib**
- **Uvicorn**

## Project Structure

```bash
app/
├── api/
│   ├── deps.py
│   └── v1/
│       ├── endpoints/
│       │   ├── health.py
│       │   ├── user/
│       │   │   └── user_routes.py
│       │   ├── product/
│       │   │   └── product_routes.py
│       │   ├── category/
│       │   │   └── category_routes.py
│       │   └── order/
│       │       └── order_routes.py
│       └── router.py
├── core/
│   ├── config.py
│   ├── security.py
│   ├── permissions.py
│   └── response.py
├── db/
│   ├── base.py
│   ├── base_class.py
│   ├── dependencies.py
│   ├── models.py
│   └── session.py
├── models/
│   ├── user.py
│   ├── category.py
│   ├── product.py
│   └── order.py
├── schemas/
│   ├── health.py
│   ├── user/
│   ├── category/
│   ├── product/
│   ├── order/
│   └── common.py
├── services/
│   ├── hello_service.py
│   ├── user/
│   ├── category/
│   ├── product/
│   └── order/
├── main.py
└── alembic/
    └── versions/
    ```
## How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```





## Environment Setup

Create a `.env` file based on `.env.example`.
