# Course Service

Course catalog microservice for the e-learning platform.

## Overview

This service is built with Express and provides course CRUD operations, instructor-based filtering, seat availability checks, and course statistics. Swagger UI is generated from inline OpenAPI annotations.

## Tech Stack

- Node.js
- Express
- CORS
- swagger-jsdoc
- swagger-ui-express

## Run Locally

```bash
cd "Swagger UI with backend/course-service"
npm install
node app.js
```

## URLs

### Direct Access

- Base URL: `http://localhost:5002`
- Swagger UI: `http://localhost:5002/api-docs`

### Via API Gateway

- Base URL: `http://localhost:8080/course-service`
- Swagger UI: `http://localhost:8080/course-service/api-docs`

## Main Files

- `app.js` - Express app, in-memory course data, and Swagger setup
- `package.json` - Node dependencies and metadata

## Endpoints

### CRUD

- `GET /courses`
- `GET /courses/{id}`
- `POST /courses`
- `PUT /courses/{id}`
- `PATCH /courses/{id}`
- `DELETE /courses/{id}`

### Filters and Analytics

- `GET /courses/instructor/{instructor}`
- `GET /courses/available`
- `GET /stats`

## Example Request Body

### Create Course

```json
{
  "name": "Database Systems",
  "code": "CS301",
  "credits": 3,
  "instructor": "Dr. Silva",
  "description": "Database design and SQL fundamentals",
  "capacity": 40
}
```

## Notes

- Course data is stored in memory, so changes reset when the server restarts.
- `name` and `code` are required when creating a course.
- Duplicate course codes are rejected.
- A course cannot be deleted while `enrolled` is greater than `0`.
