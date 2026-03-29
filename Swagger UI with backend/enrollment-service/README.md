# Enrollment Service

Member C deliverable for the MTIT Assignment 2 E-Learning Platform.

## Run

```bash
cd enrollment-service
pip install -r requirements.txt
python app.py
```

Direct URLs:

- API base: `http://localhost:5003`
- Swagger UI: `http://localhost:5003/api-docs/`
- OpenAPI JSON: `http://localhost:5003/openapi.json`

Gateway URLs after proxying:

- API base: `http://localhost:8080/enrollment-service`
- Swagger UI: `http://localhost:8080/enrollment-service/api-docs/`

## Endpoints

- `GET /health`
- `GET /enrollments`
- `GET /enrollments/<id>`
- `POST /enrollments`
- `PUT /enrollments/<id>`
- `DELETE /enrollments/<id>`
- `GET /students/<student_id>/courses`
- `GET /courses/<course_id>/students`

## Demo Requests

Create enrollment:

```json
{
  "studentId": 103,
  "courseId": 203
}
```

Mark completed:

```json
{
  "status": "completed"
}
```

## Behavior Notes

- Duplicate active or completed enrollments return `409 Conflict`.
- Deleting an enrollment performs a soft drop by setting `status` to `dropped`.
- Posting the same `studentId` and `courseId` after a drop reactivates the existing record.
- The service does not call other microservices, so demos remain stable even if teammate services are offline.
