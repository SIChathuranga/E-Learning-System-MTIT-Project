# API Gateway

Single entry point for all microservices in the e-learning platform.

## Overview

This gateway is implemented with Node.js using the built-in HTTP server. It proxies requests to all backend services, rewrites documentation-related paths so Swagger and OpenAPI pages continue to work through gateway prefixes, and performs upstream-aware health checks.

## Covered Services

| Gateway Prefix | Service | Target |
|----------------|---------|--------|
| `/student-service` | Student Service | `http://localhost:8000` |
| `/course-service` | Course Service | `http://localhost:5002` |
| `/enrollment-service` | Enrollment Service | `http://localhost:5003` |
| `/grade-service` | Grade Service | `http://localhost:5004` |

Each target can also be overridden with environment variables:

- `STUDENT_SERVICE_URL`
- `COURSE_SERVICE_URL`
- `ENROLLMENT_SERVICE_URL`
- `GRADE_SERVICE_URL`

## Run Locally

```bash
cd "Swagger UI with backend/api-gateway"
npm install
node app.js
```

## Gateway URLs

- Health: `http://localhost:8080/health`
- Root overview: `http://localhost:8080/`
- Student Service: `http://localhost:8080/student-service`
- Student Swagger: `http://localhost:8080/student-service/docs`
- Course Service: `http://localhost:8080/course-service`
- Course Swagger: `http://localhost:8080/course-service/api-docs`
- Enrollment Service: `http://localhost:8080/enrollment-service`
- Enrollment Swagger: `http://localhost:8080/enrollment-service/api-docs/`
- Grade Service: `http://localhost:8080/grade-service`
- Grade Swagger: `http://localhost:8080/grade-service/apidocs`

## Main Behavior

- Proxies incoming requests to the correct upstream service.
- Supports `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, and `OPTIONS`.
- Applies CORS headers at the gateway layer.
- Rewrites redirect and documentation asset paths for Student, Enrollment, and Grade service docs.
- Returns a summary of registered services from `/`.
- Checks upstream service availability from `/health` and reports per-service status.

## Main Files

- `app.js` - Gateway server and proxy logic
- `package.json` - Gateway metadata and start script

## Notes

- The gateway does not replace the services; each target service must still be running locally.
- If an upstream service is unavailable, the gateway returns `502 Failed to reach upstream service`.
- If one or more upstream health checks fail, the gateway `/health` endpoint returns `503` with per-service details.
