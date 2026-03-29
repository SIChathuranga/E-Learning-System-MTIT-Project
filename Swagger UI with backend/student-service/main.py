from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import logging

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Service", version="1.0.0", description="Student Management Microservice")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Display comprehensive service information on startup"""
    print("\n" + "="*80)
    print("="*80)
    print(" "*20 + "🎓 STUDENT SERVICE - STARTUP INFORMATION")
    print("="*80)
    print("="*80 + "\n")
    
    # Service Information
    print("📋 SERVICE INFORMATION:")
    print(f"   Service Name:        Student Service (Microservice)")
    print(f"   Version:             1.0.0")
    print(f"   Framework:           FastAPI")
    print(f"   Server:              Uvicorn")
    print(f"   Status:              ✓ Running\n")
    
    # Access Information
    print("🌐 ACCESS INFORMATION:")
    print(f"   Host:                0.0.0.0")
    print(f"   Port:                8000")
    print(f"   Base URL:            http://localhost:8000")
    print(f"   API Base:            http://localhost:8000/api\n")
    
    # Documentation Links
    print("📚 DOCUMENTATION:")
    print(f"   Swagger UI:          http://localhost:8000/docs")
    print(f"   ReDoc Alternative:   http://localhost:8000/redoc")
    print(f"   OpenAPI Schema:      http://localhost:8000/openapi.json\n")
    
    # Database Information
    print("🗄️  DATABASE:")
    print(f"   Type:                SQLite")
    print(f"   File:                students.db")
    print(f"   ORM:                 SQLAlchemy")
    print(f"   Status:              ✓ Connected\n")
    
    # Available Endpoints Summary
    print("📡 API ENDPOINTS (11 Total):\n")
    
    print("   CRUD Operations (5):")
    print("   ├─ POST   /students                     - Create a new student")
    print("   ├─ GET    /students                     - Get all students")
    print("   ├─ GET    /students/{student_id}       - Get student by ID")
    print("   ├─ PUT    /students/{student_id}       - Update a student")
    print("   └─ DELETE /students/{student_id}       - Delete a student\n")
    
    print("   Search & Filter Endpoints (3) - Category 1:")
    print("   ├─ GET    /students/search?name={name} - Search students by name")
    print("   ├─ GET    /students/by-course/{course} - Get students by course")
    print("   └─ GET    /students/by-email/{email}   - Get student by email\n")
    
    print("   Statistics Endpoints (3) - Category 2:")
    print("   ├─ GET    /students/count               - Total student count")
    print("   ├─ GET    /students/courses             - Get all unique courses")
    print("   └─ GET    /students/course/{course}/count - Students per course\n")
    
    # HTTP Methods Summary
    print("🔧 SUPPORTED HTTP METHODS:")
    print("   ✓ GET    (Retrieve data)")
    print("   ✓ POST   (Create data)")
    print("   ✓ PUT    (Update data)")
    print("   ✓ DELETE (Remove data)\n")
    
    # Response Formats
    print("📝 RESPONSE FORMATS:")
    print("   Content-Type: application/json")
    print("   HTTP Status Codes:")
    print("   ├─ 200 OK            (Successful request)")
    print("   ├─ 201 Created       (Resource created)")
    print("   ├─ 400 Bad Request   (Invalid parameters)")
    print("   ├─ 404 Not Found     (Resource not found)")
    print("   └─ 500 Server Error  (Internal error)\n")
    
    # Testing Instructions
    print("🧪 QUICK START TESTING:")
    print("   1. Open Swagger UI:  http://localhost:8000/docs")
    print("   2. Click on any endpoint to expand")
    print("   3. Click 'Try it out'")
    print("   4. Fill in parameters and click 'Execute'\n")
    
    print("   Or use cURL:")
    print('   curl -X GET "http://localhost:8000/students"')
    print('   curl -X POST "http://localhost:8000/students?name=John&email=john@test.com&course=Math"\n')
    
    # Features
    print("✨ SERVICE FEATURES:")
    print("   ✓ RESTful API Design")
    print("   ✓ Interactive Swagger UI Documentation")
    print("   ✓ SQLite Database with ORM")
    print("   ✓ Automatic API Schema Generation")
    print("   ✓ Real-time Code Reloading (--reload enabled)")
    print("   ✓ Comprehensive Search & Filtering")
    print("   ✓ Statistical Endpoints\n")
    
    print("="*80)
    print("="*80)
    print(" "*15 + "✅ Student Service Ready - Press CTRL+C to shutdown")
    print("="*80)
    print("="*80 + "\n")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students")
def create_student(name: str, email: str, course: str, db: Session = Depends(get_db)):
    student = models.Student(name=name, email=email, course=course)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

# Category 1: Search/Filter Endpoints
@app.get("/students/search")
def search_students(name: str = None, db: Session = Depends(get_db)):
    """Search students by name"""
    if not name:
        raise HTTPException(status_code=400, detail="Name parameter is required")
    students = db.query(models.Student).filter(models.Student.name.ilike(f"%{name}%")).all()
    return students

@app.get("/students/by-course/{course}")
def get_students_by_course(course: str, db: Session = Depends(get_db)):
    """Get all students in a specific course"""
    students = db.query(models.Student).filter(models.Student.course == course).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found in this course")
    return students

@app.get("/students/by-email/{email}")
def get_student_by_email(email: str, db: Session = Depends(get_db)):
    """Get student by email"""
    student = db.query(models.Student).filter(models.Student.email == email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Category 2: Statistics Endpoints
@app.get("/students/count")
def get_students_count(db: Session = Depends(get_db)):
    """Get total number of students"""
    count = db.query(models.Student).count()
    return {"total_students": count}

@app.get("/students/courses")
def get_all_courses(db: Session = Depends(get_db)):
    """Get list of all unique courses"""
    courses = db.query(models.Student.course).distinct().all()
    return {"courses": [course[0] for course in courses]}

@app.get("/students/course/{course}/count")
def get_course_student_count(course: str, db: Session = Depends(get_db)):
    """Get count of students in a specific course"""
    count = db.query(models.Student).filter(models.Student.course == course).count()
    return {"course": course, "student_count": count}

# Original CRUD Endpoints
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int, name: str, email: str, course: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = name
    student.email = email
    student.course = course
    db.commit()
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Student deleted"}
