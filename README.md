# BucketList API

A RESTful API for managing bucket lists - things you want to do before you die.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.9+-blue)
![Flask Version](https://img.shields.io/badge/flask-2.3.0-blue)

## Features

- User authentication with JWT tokens
- Create, read, update, and delete bucket lists
- Add items to bucket lists
- Mark items as done/undone
- Pagination support
- Search functionality
- RESTful API design
- Swagger API documentation
- Comprehensive test coverage

## Technology Stack

**Backend:**
- Python 3.9+
- Flask 2.3.0
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-Migrate
- PyJWT
- PostgreSQL/SQLite

**Frontend:**
- AngularJS 1.8.3
- Bootstrap 5
- HTML5/CSS3

## Installation

### Prerequisites

- Python 3.9 or higher
- Node.js 14 or higher
- PostgreSQL (optional, SQLite for development)

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bucketlist-api.git
cd bucketlist-api
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize database:
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

6. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

The application will be available at `http://localhost:8080`

## API Documentation

Interactive API documentation is available at: `http://localhost:5000/apidocs/`

### API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/v1/auth/register` | POST | Register a new user | No |
| `/api/v1/auth/login` | POST | Login user | No |
| `/api/v1/bucketlists` | POST | Create bucket list | Yes |
| `/api/v1/bucketlists` | GET | Get all bucket lists | Yes |
| `/api/v1/bucketlists/<id>` | GET | Get single bucket list | Yes |
| `/api/v1/bucketlists/<id>` | PUT | Update bucket list | Yes |
| `/api/v1/bucketlists/<id>` | DELETE | Delete bucket list | Yes |
| `/api/v1/bucketlists/<id>/items` | POST | Add item to bucket list | Yes |
| `/api/v1/bucketlists/<id>/items/<item_id>` | PUT | Update bucket list item | Yes |
| `/api/v1/bucketlists/<id>/items/<item_id>` | DELETE | Delete bucket list item | Yes |

### Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header: