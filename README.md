# Library Management System API

A comprehensive API for managing library resources, built with FastAPI and PostgreSQL.

## Features

- **Book Management**: Add, update, delete, and search books by various criteria.
- **Member Management**: Register, update, and manage library members.
- **Loan System**: Check out books to members, track returns, and monitor overdue loans.
- **RESTful API**: Modern, fully-documented REST API with interactive documentation.

## Tech Stack

- **FastAPI**: High-performance web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **PostgreSQL**: Robust relational database
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server implementation

## Project Structure

```
library_management_system/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── books.py
│   │       ├── members.py
│   │       └── loans.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── loan.py
│   │
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── loan.py
│   │
│   └── database/
│       ├── __init__.py
│       └── db.py
│
├── requirements.txt
└── .env
```

## Installation and Setup

### Prerequisites

- Python 3.9+
- PostgreSQL

### Environment Setup

1. Clone the repository:
   ```bash
   cd Backend-Using-FastAPI
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following content:
   ```
   DATABASE_URL=postgresql://username:password@localhost/library_db
   ```
   Replace `username`, `password`, and `library_db` with your PostgreSQL credentials.

### Database Setup

1. Create a PostgreSQL database:
   ```sql
   CREATE DATABASE library_db;
   ```

### Running the Application

1. Start the application:
   ```bash
   python run.py
   ```

2. The API will be available at `http://localhost:8000`
3. Interactive API documentation is available at `http://localhost:8000/docs`

## API Endpoints

### Books

- `GET /api/v1/books` - List all books (with optional filtering)
- `GET /api/v1/books/{book_id}` - Get a specific book
- `POST /api/v1/books` - Add a new book
- `PUT /api/v1/books/{book_id}` - Update a book
- `DELETE /api/v1/books/{book_id}` - Delete a book

### Members

- `GET /api/v1/members` - List all members (with optional filtering)
- `GET /api/v1/members/{member_id}` - Get a specific member
- `POST /api/v1/members` - Register a new member
- `PUT /api/v1/members/{member_id}` - Update a member
- `DELETE /api/v1/members/{member_id}` - Delete a member

### Loans

- `GET /api/v1/loans` - List all loans (with optional filtering)
- `GET /api/v1/loans/{loan_id}` - Get a specific loan
- `GET /api/v1/loans/overdue` - List all overdue loans
- `POST /api/v1/loans` - Create a new loan (check out a book)
- `PUT /api/v1/loans/{loan_id}` - Update a loan (return a book)
- `DELETE /api/v1/loans/{loan_id}` - Delete a loan record

## Example Usage

### Creating a Book

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/books/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "9780743273565",
  "publication_year": 1925,
  "genre": "Classic Fiction",
  "description": "A story of wealth, love, and the American Dream."
}'
```

### Creating a Member

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/members/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "123-456-7890",
  "address": "123 Main St, Anytown, CA"
}'
```

### Creating a Loan (Borrowing a Book)

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/loans/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "book_id": 1,
  "member_id": 1
}'
```

## Development

### Adding New Features

1. Create or modify models in `app/models/models.py`
2. Update or create schemas in `app/schemas/`
3. Implement CRUD operations in `app/crud/`
4. Add API endpoints in `app/api/routes/`
5. Implement react

