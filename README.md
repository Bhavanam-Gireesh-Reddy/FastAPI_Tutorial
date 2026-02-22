# FastAPI Tutorial

A comprehensive project for learning and implementing FastAPI, covering everything from basic routing to advanced topics like SQL database integration, OAuth2 authentication with JWT, and containerization with Docker.

## 🚀 Features

- **FastAPI Basics**: Implementation of path and query parameters, and Pydantic request bodies.
- **CRUD Operations**: A complete book management system using an in-memory list and SQLAlchemy.
- **Database Integration**: Connection to MySQL using SQLAlchemy and environment variables.
- **Authentication & Authorization**:
  - User signup and login with password hashing.
  - JWT (JSON Web Token) generation and validation.
  - Role-based access control (Admin/User).
- **Docker Support**: Dockerfile and Docker Compose configurations for easy deployment.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: MySQL, [SQLAlchemy](https://www.sqlalchemy.org/) (ORM)
- **Security**: Python-jose (JWT), Passlib (Password hashing)
- **Environment Management**: Python-dotenv
- **Containerization**: Docker, Docker Compose

## 📁 Project Structure

```text
FastAPI_Tutorial/
├── auth/                   # Authentication & Authorization logic
│   ├── auth_database.py    # Auth-specific database connection
│   ├── models.py           # SQL Alchemy user models
│   ├── schemas.py          # Pydantic schemas for Auth
│   ├── utils.py            # Password hashing and verification
│   └── main.py             # Auth endpoints (signup, login, protected)
├── CURD.py                 # CRUD implementation with in-memory list
├── database.py             # Main database connection setup
├── model.py                # Main application models (e.g., Book)
├── main.py                 # Entry point for basic routing and examples
├── project.py              # Main application with database integration
├── dockerfile              # Docker image configuration
├── docker-compose.yml      # Multi-container orchestration
├── requirements.txt        # Project dependencies
└── .env                    # Environment variables (to be created)
```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FastAPI_Tutorial
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory and add the following:

```env
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=your_db_name

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Ensure your MySQL server is running and the database specified in `.env` exists. You can use `create_table.py` to initialize tables if needed.

## 🏃 How to Run

### Run Locally

You can run different parts of the tutorial using `uvicorn`:

```bash
# Basic FastAPI examples
uvicorn main:app --reload

# CRUD with in-memory list
uvicorn CURD:app --reload

# Full project with Database
uvicorn project:app --reload

# Authentication system
uvicorn auth.main:app --reload
```

### Run with Docker

```bash
docker-compose up --build
```

## 🔌 API Endpoints (Quick Overview)

### General

- `GET /`: Home endpoint
- `GET /greet/{name}`: Greeting with path parameter

### Book Management (CRUD)

- `GET /books`: List all books
- `POST /books`: Create a new book
- `PUT /books/{id}`: Update a book
- `DELETE /books/{id}`: Delete a book

### Authentication

- `POST /signup`: Register a new user
- `POST /login`: Login and receive access token
- `GET /protected`: Access a JWT protected route

---
Developed by Bhavanam Gireesh Reddy.
