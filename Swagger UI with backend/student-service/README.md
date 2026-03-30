# Student Service

Student management microservice for the e-learning platform.

## Overview

This service is built with FastAPI and SQLAlchemy. It manages student records and provides search, filtering, and statistics endpoints.

## Tech Stack

- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite

## Run Locally

```bash
cd "Swagger UI with backend/student-service"
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## URLs

### Direct Access

- Base URL: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### Via API Gateway

- Base URL: `http://localhost:8080/student-service`
- Swagger UI: `http://localhost:8080/student-service/docs`
- OpenAPI JSON: `http://localhost:8080/student-service/openapi.json`

## Main Files

- `main.py` - FastAPI application and route definitions
- `database.py` - SQLAlchemy database configuration
- `models.py` - Student model definition
- `students.db` - SQLite database created at runtime

## Endpoints

### CRUD

- `POST /students`
- `GET /students`
- `GET /students/{student_id}`
- `PUT /students/{student_id}`
- `DELETE /students/{student_id}`

### Search and Filters

- `GET /students/search?name={name}`
- `GET /students/by-course/{course}`
- `GET /students/by-email/{email}`

### Statistics

- `GET /students/count`
- `GET /students/courses`
- `GET /students/course/{course}/count`

## Request Patterns

This service uses query parameters for create and update operations instead of JSON bodies.

### Create Student

```bash
curl -X POST "http://localhost:8000/students?name=John%20Doe&email=john@example.com&course=SE"
```

### Update Student

```bash
curl -X PUT "http://localhost:8000/students/1?name=John%20Doe&email=john@example.com&course=IT"
```

## Notes

- Tables are created automatically on startup.
- The service returns `404` when a student, course grouping, or email lookup does not exist.
- The search endpoint returns `400` if the `name` query parameter is missing.
