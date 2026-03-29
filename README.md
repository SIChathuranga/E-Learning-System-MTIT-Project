# E-Learning-System-MTIT-Project

E-Learning platform built with four microservices and a shared API Gateway.

## Architecture Overview

```text
                    API Gateway (Port 8080)
               Single entry point for all requests

        Student        Course        Enrollment        Grade
        Service        Service        Service         Service
        Port 8000      Port 5002      Port 5003       Port 5004
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
│   ├── requirements.txt
│   ├── database.py
│   └── models.py
├── course-service/
│   ├── app.js
│   ├── package.json
│   └── package-lock.json
├── enrollment-service/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
└── grade-service/
    ├── app.py
    ├── requirements.txt
    ├── swagger.py
    ├── database.py
    └── models.py
```

## Team Responsibilities

| Member | Microservice | Primary Responsibilities | Main API Endpoints |
|--------|--------------|--------------------------|--------------------|
| Member A | Student Service | Student profiles, search, filtering, analytics | `/students`, `/students/search`, `/students/by-course/{course}`, `/students/by-email/{email}`, `/students/count`, `/students/courses`, `/students/course/{course}/count` |
| Member B | Course Service | Course catalog and instructor management | `/courses`, `/courses/instructor/{instructor}`, `/courses/available`, `/stats` |
| Member C | Enrollment Service | Student enrollment lifecycle and mapping queries | `/health`, `/enrollments`, `/students/{studentId}/courses`, `/courses/{courseId}/students` |
| Member D | Grade Service | Grade CRUD, availability, instructor filtering, GPA analytics | `/health`, `/grades`, `/grades/enrollment/{enrollment_id}`, `/grades/instructor/{instructor}`, `/grades/availability/{enrollment_id}`, `/grades/gpa/{enrollment_id}`, `/grades/gpa/overall` |

## Technology Stack

- Python 3.8+
- FastAPI for `student-service`
- Flask for `enrollment-service` and `grade-service`
- Node.js / Express for `course-service`
- Node.js HTTP server for `api-gateway`
- SQLite / SQLAlchemy where applicable
- Swagger UI / OpenAPI docs per service

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- `pip`
- `npm`

### Installation

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

### Running the Services

Start each service in a separate terminal:

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

| Service | Base URL | Swagger UI |
|---------|----------|------------|
| Student Service | `http://localhost:8000` | `http://localhost:8000/docs` |
| Course Service | `http://localhost:5002` | `http://localhost:5002/api-docs` |
| Enrollment Service | `http://localhost:5003` | `http://localhost:5003/api-docs/` |
| Grade Service | `http://localhost:5004` | `http://localhost:5004/apidocs` |

### Via API Gateway

| Service | Base URL | Swagger UI |
|---------|----------|------------|
| Student Service | `http://localhost:8080/student-service` | `http://localhost:8080/student-service/docs` |
| Course Service | `http://localhost:8080/course-service` | `http://localhost:8080/course-service/api-docs` |
| Enrollment Service | `http://localhost:8080/enrollment-service` | `http://localhost:8080/enrollment-service/api-docs/` |
| Grade Service | `http://localhost:8080/grade-service` | `http://localhost:8080/grade-service/apidocs` |

### Health Check

`http://localhost:8080/health`

## API Gateway Notes

- The gateway forwards requests to all four microservices.
- Supported methods include `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, and `OPTIONS`.
- CORS headers are applied at the gateway.
- Redirect and documentation asset paths are rewritten so Swagger/OpenAPI pages work correctly through gateway prefixes.

## Assignment Checklist

- [ ] All 4 services run without errors
- [ ] API Gateway runs without errors
- [ ] Each service Swagger UI is accessible directly
- [ ] Each service Swagger UI is accessible via gateway
- [ ] CRUD operations work in Postman
- [ ] Folder structure matches requirements
- [ ] Slide deck includes screenshots and contribution details

## License

This project is for educational purposes as part of IT4020 - Modern Topics in IT.
