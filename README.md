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
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── student-service/           (Member A)
│   ├── app.py
│   ├── requirements.txt
│   ├── swagger.py
│   ├── models.py
│   └── database.py
│
├── course-service/            (Member B)
│   ├── app.py
│   ├── requirements.txt
│   ├── swagger.py
│   ├── models.py
│   └── database.py
│
├── enrollment-service/       (Member C)
│   ├── app.py
│   ├── requirements.txt
│   ├── swagger.py
│   ├── models.py
│   └── database.py
│
└── grade-service/            (Member D)
    ├── app.py
    ├── requirements.txt
    ├── swagger.py
    ├── models.py
    └── database.py
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

- **Language:** Python 3.8+
- **Framework:** Flask
- **Database:** SQLite (via SQLAlchemy ORM)
- **API Documentation:** Swagger UI (via flasgger)
- **Gateway:** Flask with custom routing

---

## Database Design

Each microservice has its own SQLite database file for data persistence:

### Student Service Database (`student_service.db`)
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Course Service Database (`course_service.db`)
```sql
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    instructor VARCHAR(100),
    credits INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Enrollment Service Database (`enrollment_service.db`)
```sql
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);
```

### Grade Service Database (`grade_service.db`)
```sql
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_id INTEGER NOT NULL,
    grade VARCHAR(5),
    feedback TEXT,
    graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python Package Manager)

### Installation

1. Clone the repository
2. Install dependencies for each service:

```bash
# Install API Gateway dependencies
cd "Swagger UI with backend/api-gateway"
pip install -r requirements.txt

# Install Student Service dependencies
cd ../student-service
pip install -r requirements.txt

# Install Course Service dependencies
cd ../course-service
pip install -r requirements.txt

# Install Enrollment Service dependencies
cd ../enrollment-service
pip install -r requirements.txt

# Install Grade Service dependencies
cd ../grade-service
pip install -r requirements.txt
```

### Running the Services

Start each service in separate terminals:

```bash
# Terminal 1 - API Gateway (Port 8080)
cd "Swagger UI with backend/api-gateway"
python app.py

# Terminal 2 - Student Service (Port 5001)
cd "Swagger UI with backend/student-service"
python app.py

# Terminal 3 - Course Service (Port 5002)
cd "Swagger UI with backend/course-service"
python app.py

# Terminal 4 - Enrollment Service (Port 5003)
cd "Swagger UI with backend/enrollment-service"
python app.py

# Terminal 5 - Grade Service (Port 5004)
cd "Swagger UI with backend/grade-service"
python app.py
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
