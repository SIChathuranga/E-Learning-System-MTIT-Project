# Grade Service

Grade management microservice for the e-learning platform.

## Overview

This service is built with Flask, Flask-SQLAlchemy, and Flasgger. It manages grade records, supports instructor-based filtering, checks grade availability, and calculates GPA values.

## Tech Stack

- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Flasgger
- SQLite

## Run Locally

```bash
cd "Swagger UI with backend/grade-service"
pip install -r requirements.txt
python app.py
```

## URLs

### Direct Access

- Base URL: `http://localhost:5004`
- Swagger UI: `http://localhost:5004/apidocs`
- Legacy Swagger redirect: `http://localhost:5004/api-docs`
- Health: `http://localhost:5004/health`

### Via API Gateway

- Base URL: `http://localhost:8080/grade-service`
- Swagger UI: `http://localhost:8080/grade-service/apidocs`
- Health: `http://localhost:8080/grade-service/health`

## Main Files

- `app.py` - Flask app and all grade endpoints
- `database.py` - Database initialization
- `models.py` - Grade model
- `swagger.py` - Flasgger template and config

## Endpoints

### Health

- `GET /health`

### Grade CRUD

- `GET /grades`
- `GET /grades/{grade_id}`
- `POST /grades`
- `PUT /grades/{grade_id}`
- `DELETE /grades/{grade_id}`

### Queries and Analytics

- `GET /grades/enrollment/{enrollment_id}`
- `GET /grades/instructor/{instructor}`
- `GET /grades/availability/{enrollment_id}`
- `GET /grades/gpa/{enrollment_id}`
- `GET /grades/gpa/overall`

## Example Request Body

### Create Grade

```json
{
  "enrollment_id": 1,
  "instructor": "Dr. Silva",
  "grade": "A",
  "feedback": "Excellent performance"
}
```

## Notes

- Data is stored in SQLite through SQLAlchemy.
- Only one grade record is allowed per `enrollment_id`.
- GPA is calculated from letter grades using an internal grade-point mapping.
- The service includes detailed logging for requests, responses, errors, and database actions.
