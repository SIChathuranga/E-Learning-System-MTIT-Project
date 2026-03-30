# Enrollment Service

Enrollment management microservice for the e-learning platform.

## Overview

This service is built with Flask and keeps enrollment data in memory. It manages the student-course relationship, supports enrollment creation and updates, and exposes a lightweight OpenAPI documentation page.

## Tech Stack

- Flask
- Flask-CORS
- In-memory data store
- OpenAPI 3.0 JSON + embedded Swagger UI page

## Run Locally

```bash
cd "Swagger UI with backend/enrollment-service"
pip install -r requirements.txt
python app.py
```

## URLs

### Direct Access

- Base URL: `http://localhost:5003`
- Swagger UI: `http://localhost:5003/api-docs/`
- OpenAPI JSON: `http://localhost:5003/openapi.json`
- Health: `http://localhost:5003/health`

### Via API Gateway

- Base URL: `http://localhost:8080/enrollment-service`
- Swagger UI: `http://localhost:8080/enrollment-service/api-docs/`
- OpenAPI JSON: `http://localhost:8080/enrollment-service/openapi.json`
- Health: `http://localhost:8080/enrollment-service/health`

## Main Files

- `app.py` - Flask routes, OpenAPI spec, and in-memory enrollment state
- `requirements.txt` - Python dependencies

## Endpoints

### Health

- `GET /health`

### Enrollment CRUD

- `GET /enrollments`
- `GET /enrollments/{id}`
- `POST /enrollments`
- `PUT /enrollments/{id}`
- `DELETE /enrollments/{id}`

### Relationship Queries

- `GET /students/{studentId}/courses`
- `GET /courses/{courseId}/students`

## Example Request Bodies

### Create Enrollment

```json
{
  "studentId": 103,
  "courseId": 203
}
```

### Update Enrollment Status

```json
{
  "status": "completed"
}
```

## Notes

- `POST /enrollments` creates a new enrollment or reactivates a previously dropped one.
- Duplicate active or completed enrollments return `409 Conflict`.
- `DELETE /enrollments/{id}` is a soft delete that changes the status to `dropped`.
- Data is stored in memory, so the state resets when the service restarts.
