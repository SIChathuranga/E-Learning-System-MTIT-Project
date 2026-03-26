# E-Learning-System-MTIT-Project

E-Learning platform will have **4 microservices** (one per member) and an **API Gateway**

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    API Gateway (Port 8080)              │
│              Single entry point for all requests        │
└─────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Student   │ │   Course    │ │ Enrollment  │ │   Grade     │
│  Service    │ │  Service    │ │  Service    │ │  Service    │
│  Port 5001  │ │  Port 5002  │ │  Port 5003  │ │  Port 5004  │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

---

## Project Structure

```
Swagger UI with backend/
├── api-gateway/
│   ├── app.js
│   ├── package.json
│   └── README.md
│
├── student-service/           (Member A)
│   ├── app.js
│   ├── package.json
│   ├── swagger.js
│   └── data/
│       └── students.js (in-memory database)
│
├── course-service/            (Member B)
│   ├── app.js
│   ├── package.json
│   ├── swagger.js
│   └── data/
│       └── courses.js
│
├── enrollment-service/       (Member C)
│   ├── app.js
│   ├── package.json
│   ├── swagger.js
│   └── data/
│       └── enrollments.js
│
└── grade-service/            (Member D)
    ├── app.js
    ├── package.json
    ├── swagger.js
    └── data/
        └── grades.js
```

---

## Team Responsibilities

| Member | Microservice | Primary Responsibilities | API Endpoints |
|--------|--------------|------------------------|---------------|
| Member A | Student Service | Manage student profiles, registration, authentication | GET/POST/PUT/DELETE /students |
| Member B | Course Service | Manage course catalog, course details, instructors | GET/POST/PUT/DELETE /courses |
| Member C | Enrollment Service | Handle student enrollments, drop courses, enrollment history | GET/POST/DELETE /enrollments |
| Member D | Grade Service | Manage grades, grade submissions, grade reports | GET/POST/PUT /grades |

---

## Technology Stack

- **Runtime:** Node.js
- **Framework:** Express.js
- **API Documentation:** Swagger UI
- **Gateway:** http-proxy-middleware

---

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm (Node Package Manager)

### Installation

1. Clone the repository
2. Install dependencies for each service:

```bash
# Install API Gateway dependencies
cd Swagger UI with backend/api-gateway
npm install

# Install Student Service dependencies
cd ../student-service
npm install

# Install Course Service dependencies
cd ../course-service
npm install

# Install Enrollment Service dependencies
cd ../enrollment-service
npm install

# Install Grade Service dependencies
cd ../grade-service
npm install
```

### Running the Services

Start each service in separate terminals:

```bash
# Terminal 1 - API Gateway (Port 8080)
cd Swagger UI with backend/api-gateway
node app.js

# Terminal 2 - Student Service (Port 5001)
cd Swagger UI with backend/student-service
node app.js

# Terminal 3 - Course Service (Port 5002)
cd Swagger UI with backend/course-service
node app.js

# Terminal 4 - Enrollment Service (Port 5003)
cd Swagger UI with backend/enrollment-service
node app.js

# Terminal 5 - Grade Service (Port 5004)
cd Swagger UI with backend/grade-service
node app.js
```

---

## API Access

### Direct Access (Individual Services)

| Service | URL | Swagger UI |
|---------|-----|------------|
| Student Service | http://localhost:5001 | http://localhost:5001/api-docs |
| Course Service | http://localhost:5002 | http://localhost:5002/api-docs |
| Enrollment Service | http://localhost:5003 | http://localhost:5003/api-docs |
| Grade Service | http://localhost:5004 | http://localhost:5004/api-docs |

### Via API Gateway

| Service | URL | Swagger UI |
|---------|-----|------------|
| Student Service | http://localhost:8080/student-service | http://localhost:8080/student-service/api-docs |
| Course Service | http://localhost:8080/course-service | http://localhost:8080/course-service/api-docs |
| Enrollment Service | http://localhost:8080/enrollment-service | http://localhost:8080/enrollment-service/api-docs |
| Grade Service | http://localhost:8080/grade-service | http://localhost:8080/grade-service/api-docs |

### Health Check
```
http://localhost:8080/health
```

---

## Assignment Requirements

- [ ] All 4 services run without errors
- [ ] API Gateway runs without errors
- [ ] Each service's Swagger UI accessible directly (4 screenshots)
- [ ] Each service's Swagger UI accessible via gateway (4 screenshots)
- [ ] All CRUD operations work (test with Postman)
- [ ] Folder structure matches requirements
- [ ] Slide deck is professional with all screenshots
- [ ] Individual contributions clearly listed

---

## License

This project is for educational purposes as part of IT4020 - Modern Topics in IT.
