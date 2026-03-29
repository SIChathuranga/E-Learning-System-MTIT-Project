# API Gateway

This gateway is the single entry point for all four microservices in the assignment.

## Covered Services

- `student-service` -> `http://localhost:8000`
- `course-service` -> `http://localhost:5002`
- `enrollment-service` -> `http://localhost:5003`
- `grade-service` -> `http://localhost:5004`

## Run

```bash
cd "Swagger UI with backend/api-gateway"
node app.js
```

## Gateway URLs

- Health: `http://localhost:8080/health`
- Student Service: `http://localhost:8080/student-service`
- Student Swagger: `http://localhost:8080/student-service/docs`
- Course Service: `http://localhost:8080/course-service`
- Course Swagger: `http://localhost:8080/course-service/api-docs`
- Enrollment Service: `http://localhost:8080/enrollment-service`
- Enrollment Swagger: `http://localhost:8080/enrollment-service/api-docs/`
- Grade Service: `http://localhost:8080/grade-service`
- Grade Swagger: `http://localhost:8080/grade-service/apidocs`

## Notes

- All request methods are forwarded, including `GET`, `POST`, `PUT`, `PATCH`, and `DELETE`.
- CORS headers are applied at the gateway level.
- Redirects and Swagger/OpenAPI asset paths are adjusted so the docs pages still work through the gateway prefixes.
