# E-Learning System MTIT Project

This repository contains an e-learning platform built with four microservices and a lightweight API Gateway.

## Architecture Overview

```text
                    API Gateway (Port 8080)
               Single entry point for all requests

        Student        Course        Enrollment        Grade
        Service        Service       Service           Service
        Port 8000      Port 5002     Port 5003         Port 5004
```

## Project Structure

```text
Swagger UI with backend/
├── api-gateway/
│   ├── app.js
│   ├── package.json
│   └── README.md
├── student-service/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── requirements.txt
│   └── README.md
├── course-service/
│   ├── app.js
│   ├── package.json
│   ├── package-lock.json
│   └── README.md
├── enrollment-service/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
└── grade-service/
    ├── app.py
    ├── database.py
    ├── models.py
    ├── swagger.py
    ├── requirements.txt
    └── README.md
```

## Services

| Service | Tech Stack | Port | README |
|---------|------------|------|--------|
| API Gateway | Node.js HTTP server | 8080 | [api-gateway/README.md](./Swagger%20UI%20with%20backend/api-gateway/README.md) |
| Student Service | FastAPI + SQLAlchemy + SQLite | 8000 | [student-service/README.md](./Swagger%20UI%20with%20backend/student-service/README.md) |
| Course Service | Express + Swagger UI | 5002 | [course-service/README.md](./Swagger%20UI%20with%20backend/course-service/README.md) |
| Enrollment Service | Flask + in-memory data + OpenAPI UI | 5003 | [enrollment-service/README.md](./Swagger%20UI%20with%20backend/enrollment-service/README.md) |
| Grade Service | Flask + SQLAlchemy + Flasgger | 5004 | [grade-service/README.md](./Swagger%20UI%20with%20backend/grade-service/README.md) |

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- `pip`
- `npm`

## Installation

Install dependencies inside each service folder:

```bash
# API Gateway
cd "Swagger UI with backend/api-gateway"
npm install

# Student Service
cd ../student-service
pip install -r requirements.txt

# Course Service
cd ../course-service
npm install

# Enrollment Service
cd ../enrollment-service
pip install -r requirements.txt

# Grade Service
cd ../grade-service
pip install -r requirements.txt
```

## Running the System

Start each component in a separate terminal:

```bash
# Terminal 1 - API Gateway
cd "Swagger UI with backend/api-gateway"
node app.js

# Terminal 2 - Student Service
cd "Swagger UI with backend/student-service"
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3 - Course Service
cd "Swagger UI with backend/course-service"
node app.js

# Terminal 4 - Enrollment Service
cd "Swagger UI with backend/enrollment-service"
python app.py

# Terminal 5 - Grade Service
cd "Swagger UI with backend/grade-service"
python app.py
```

## API Access

### Direct Access

| Service | Base URL | Swagger / OpenAPI UI |
|---------|----------|----------------------|
| Student Service | `http://localhost:8000` | `http://localhost:8000/docs` |
| Course Service | `http://localhost:5002` | `http://localhost:5002/api-docs` |
| Enrollment Service | `http://localhost:5003` | `http://localhost:5003/api-docs/` |
| Grade Service | `http://localhost:5004` | `http://localhost:5004/apidocs` |

### Via API Gateway

| Service | Gateway Base URL | Swagger / OpenAPI UI |
|---------|------------------|----------------------|
| Student Service | `http://localhost:8080/student-service` | `http://localhost:8080/student-service/docs` |
| Course Service | `http://localhost:8080/course-service` | `http://localhost:8080/course-service/api-docs` |
| Enrollment Service | `http://localhost:8080/enrollment-service` | `http://localhost:8080/enrollment-service/api-docs/` |
| Grade Service | `http://localhost:8080/grade-service` | `http://localhost:8080/grade-service/apidocs` |

Gateway health check:

`http://localhost:8080/health`

## Core Responsibilities

| Service | Responsibilities | Main Endpoints |
|---------|------------------|----------------|
| Student Service | Student CRUD, search, filtering, course-based lookups, counts | `/students`, `/students/search`, `/students/by-course/{course}`, `/students/by-email/{email}`, `/students/count` |
| Course Service | Course CRUD, instructor filtering, seat availability, statistics | `/courses`, `/courses/{id}`, `/courses/instructor/{instructor}`, `/courses/available`, `/stats` |
| Enrollment Service | Enrollment creation, updates, drops, student-course mapping | `/health`, `/enrollments`, `/enrollments/{id}`, `/students/{studentId}/courses`, `/courses/{courseId}/students` |
| Grade Service | Grade CRUD, grade availability, instructor filtering, GPA calculations | `/health`, `/grades`, `/grades/enrollment/{enrollment_id}`, `/grades/instructor/{instructor}`, `/grades/availability/{enrollment_id}`, `/grades/gpa/{enrollment_id}`, `/grades/gpa/overall` |

## Notes About the API Gateway

- The gateway forwards requests to all four microservices.
- It supports `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, and `OPTIONS`.
- CORS headers are applied at the gateway level.
- Documentation asset paths are rewritten so Swagger and OpenAPI pages work through the gateway prefixes.

## Assignment Checklist

- [ ] All four services run without errors
- [ ] API Gateway runs without errors
- [ ] Swagger or OpenAPI UI is accessible directly for each service
- [ ] Swagger or OpenAPI UI is accessible through the API Gateway
- [ ] CRUD operations can be tested in Postman
- [ ] README files exist for each microservice
- [ ] Slide deck includes screenshots and contribution details

## License

This project is for educational purposes as part of IT4020 - Modern Topics in IT.
