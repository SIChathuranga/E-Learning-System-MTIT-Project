from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flasgger import Swagger
from database import db, init_db
from models import Grade
from swagger import swagger_template, swagger_config
import logging
from datetime import datetime
import time
import traceback

app = Flask(__name__)
CORS(app)

# Configure logging with enhanced format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize Swagger
swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Initialize Database
init_db(app)

# Helper function to log comprehensive request details
def log_request_details(endpoint_name, additional_info=None):
    """Log comprehensive request details with formatted sections."""
    logger.info('╔' + '═' * 78 + '╗')
    logger.info(f'║ {endpoint_name:^78} ║')
    logger.info('╠' + '═' * 78 + '╣')
    logger.info(f'║ 📅 Timestamp: {datetime.now().isoformat():<63} ║')
    logger.info(f'║ 🔧 Method: {request.method:<67} ║')
    logger.info(f'║ 📍 Endpoint: {request.path:<65} ║')
    logger.info(f'║ 🌐 Client IP: {request.remote_addr:<64} ║')
    logger.info(f'║ 🔗 URL: {request.url[:70]:<70} ║')
    
    # Log query parameters if present
    if request.args:
        logger.info(f'║ ❓ Query Parameters:{"":<57} ║')
        for key, value in request.args.items():
            logger.info(f'║    • {key}: {str(value)[:65]:<65} ║')
    
    # Log headers (filtered for security)
    logger.info(f'║ 📋 Headers:{"":<67} ║')
    safe_headers = ['Content-Type', 'Accept', 'User-Agent', 'Origin']
    for header in safe_headers:
        if header in request.headers:
            logger.info(f'║    • {header}: {str(request.headers[header])[:60]:<60} ║')
    
    # Log additional info if provided
    if additional_info:
        logger.info(f'║ 📝 Additional Info:{"":<59} ║')
        for key, value in additional_info.items():
            logger.info(f'║    • {key}: {str(value)[:60]:<60} ║')
    
    logger.info('╚' + '═' * 78 + '╝')

# Helper function to log comprehensive response details
def log_response_details(status_code, response_data=None, execution_time=None):
    """Log comprehensive response details with formatted sections."""
    logger.info('┌' + '─' * 78 + '┐')
    logger.info(f'│ {"RESPONSE DETAILS":^78} │')
    logger.info('├' + '─' * 78 + '┤')
    logger.info(f'│ ✅ Status Code: {status_code:<62} ║')
    
    if execution_time is not None:
        logger.info(f'│ ⏱️  Execution Time: {execution_time:.4f} seconds{"":<48} │')
    
    if response_data:
        logger.info(f'│ 📦 Response Data:{"":<61} │')
        # Log response data in a readable format
        if isinstance(response_data, dict):
            for key, value in response_data.items():
                value_str = str(value)[:60]
                logger.info(f'│    • {key}: {value_str:<60} │')
        elif isinstance(response_data, list):
            logger.info(f'│    • Count: {len(response_data)} items{"":<52} │')
            if response_data:
                logger.info(f'│    • First Item: {str(response_data[0])[:55]:<55} │')
    
    logger.info('└' + '─' * 78 + '┘')

# Helper function to log error details
def log_error_details(error, context=None):
    """Log comprehensive error details with formatted sections."""
    logger.error('╔' + '═' * 78 + '╗')
    logger.error(f'║ {"ERROR DETAILS":^78} ║')
    logger.error('╠' + '═' * 78 + '╣')
    logger.error(f'║ ❌ Error Type: {type(error).__name__:<63} ║')
    logger.error(f'║ 📝 Error Message: {str(error)[:60]:<60} ║')
    
    if context:
        logger.error(f'║ 🔍 Context:{"":<67} ║')
        for key, value in context.items():
            logger.error(f'║    • {key}: {str(value)[:60]:<60} ║')
    
    logger.error(f'║ 📍 Traceback:{"":<65} ║')
    tb_lines = traceback.format_exc().split('\n')
    for line in tb_lines[:5]:  # Limit traceback lines
        if line.strip():
            logger.error(f'║    {line[:74]:<74} ║')
    
    logger.error('╚' + '═' * 78 + '╝')

# Helper function to log database operation details
def log_db_operation(operation, details=None):
    """Log database operation details."""
    logger.info('┌' + '─' * 78 + '┐')
    logger.info(f'│ {"DATABASE OPERATION":^78} │')
    logger.info('├' + '─' * 78 + '┤')
    logger.info(f'│ 🗄️  Operation: {operation:<63} │')
    
    if details:
        for key, value in details.items():
            logger.info(f'│    • {key}: {str(value)[:60]:<60} │')
    
    logger.info('└' + '─' * 78 + '┘')

# Helper function to log available API endpoints
def log_api_endpoints():
    """Log all available API endpoints."""
    logger.info('╔' + '═' * 78 + '╗')
    logger.info(f'║ {"AVAILABLE API ENDPOINTS":^78} ║')
    logger.info('╠' + '═' * 78 + '╣')
    logger.info(f'║ {"Health Check":<30} GET    /health{"":<38} ║')
    logger.info(f'║ {"Get All Grades":<30} GET    /grades{"":<39} ║')
    logger.info(f'║ {"Get Grade by ID":<30} GET    /grades/<grade_id>{"":<27} ║')
    logger.info(f'║ {"Get Grades by Enrollment":<30} GET    /grades/enrollment/<enrollment_id>{"":<13} ║')
    logger.info(f'║ {"Get Grades by Instructor":<30} GET    /grades/instructor/<instructor>{"":<15} ║')
    logger.info(f'║ {"Check Grade Availability":<30} GET    /grades/availability/<enrollment_id>{"":<12} ║')
    logger.info(f'║ {"Calculate GPA":<30} GET    /grades/gpa/<enrollment_id>{"":<20} ║')
    logger.info(f'║ {"Calculate Overall GPA":<30} GET    /grades/gpa/overall{"":<28} ║')
    logger.info(f'║ {"Create Grade":<30} POST   /grades{"":<39} ║')
    logger.info(f'║ {"Update Grade":<30} PUT    /grades/<grade_id>{"":<27} ║')
    logger.info(f'║ {"Delete Grade":<30} DELETE /grades/<grade_id>{"":<27} ║')
    logger.info('╚' + '═' * 78 + '╝')

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: Service is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: healthy
            service:
              type: string
              example: grade-service
    """
    start_time = time.time()
    log_request_details('🏥 HEALTH CHECK REQUEST')
    
    response_data = {
        'status': 'healthy',
        'service': 'grade-service',
        'timestamp': datetime.now().isoformat()
    }
    
    execution_time = time.time() - start_time
    log_response_details(200, response_data, execution_time)
    
    return jsonify(response_data), 200

# GET all grades
@app.route('/grades', methods=['GET'])
def get_all_grades():
    """
    Get all grades
    ---
    tags:
      - Grades
    responses:
      200:
        description: List of all grades
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              enrollment_id:
                type: integer
                example: 1
              grade:
                type: string
                example: A
              feedback:
                type: string
                example: Excellent performance
              graded_at:
                type: string
                format: date-time
    """
    start_time = time.time()
    log_request_details('📚 GET ALL GRADES REQUEST')
    
    try:
        log_db_operation('QUERY', {'table': 'grades', 'operation': 'SELECT ALL'})
        grades = Grade.query.all()
        
        grades_data = [grade.to_dict() for grade in grades]
        
        log_db_operation('RESULT', {'rows_returned': len(grades_data)})
        
        execution_time = time.time() - start_time
        log_response_details(200, {'count': len(grades_data), 'grades': grades_data}, execution_time)
        
        return jsonify(grades_data), 200
    except Exception as e:
        log_error_details(e, {'operation': 'get_all_grades'})
        return jsonify({'error': str(e)}), 500

# GET grade by ID
@app.route('/grades/<int:grade_id>', methods=['GET'])
def get_grade(grade_id):
    """
    Get a specific grade by ID
    ---
    tags:
      - Grades
    parameters:
      - name: grade_id
        in: path
        type: integer
        required: true
        description: The ID of the grade
    responses:
      200:
        description: Grade details
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            enrollment_id:
              type: integer
              example: 1
            grade:
              type: string
              example: A
            feedback:
              type: string
              example: Excellent performance
            graded_at:
              type: string
              format: date-time
      404:
        description: Grade not found
    """
    start_time = time.time()
    log_request_details('🔍 GET GRADE BY ID REQUEST', {'Grade ID': grade_id})
    
    try:
        log_db_operation('QUERY', {'table': 'grades', 'operation': 'SELECT BY ID', 'id': grade_id})
        grade = Grade.query.get(grade_id)
        
        if not grade:
            log_db_operation('RESULT', {'found': False, 'id': grade_id})
            execution_time = time.time() - start_time
            log_response_details(404, {'error': 'Grade not found'}, execution_time)
            return jsonify({'error': 'Grade not found'}), 404
        
        grade_data = grade.to_dict()
        log_db_operation('RESULT', {'found': True, 'data': grade_data})
        
        execution_time = time.time() - start_time
        log_response_details(200, grade_data, execution_time)
        
        return jsonify(grade_data), 200
    except Exception as e:
        log_error_details(e, {'operation': 'get_grade', 'grade_id': grade_id})
        return jsonify({'error': str(e)}), 500

# GET grades by enrollment ID
@app.route('/grades/enrollment/<int:enrollment_id>', methods=['GET'])
def get_grades_by_enrollment(enrollment_id):
    """
    Get all grades for a specific enrollment
    ---
    tags:
      - Grades
    parameters:
      - name: enrollment_id
        in: path
        type: integer
        required: true
        description: The enrollment ID
    responses:
      200:
        description: List of grades for the enrollment
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              enrollment_id:
                type: integer
                example: 1
              grade:
                type: string
                example: A
              feedback:
                type: string
                example: Excellent performance
              graded_at:
                type: string
                format: date-time
    """
    start_time = time.time()
    log_request_details('📋 GET GRADES BY ENROLLMENT ID REQUEST', {'Enrollment ID': enrollment_id})
    
    try:
        log_db_operation('QUERY', {'table': 'grades', 'operation': 'SELECT BY ENROLLMENT ID', 'enrollment_id': enrollment_id})
        grades = Grade.query.filter_by(enrollment_id=enrollment_id).all()
        
        grades_data = [grade.to_dict() for grade in grades]
        log_db_operation('RESULT', {'rows_returned': len(grades_data), 'enrollment_id': enrollment_id})
        
        execution_time = time.time() - start_time
        log_response_details(200, {'count': len(grades_data), 'grades': grades_data}, execution_time)
        
        return jsonify(grades_data), 200
    except Exception as e:
        log_error_details(e, {'operation': 'get_grades_by_enrollment', 'enrollment_id': enrollment_id})
        return jsonify({'error': str(e)}), 500


# GET grades by instructor
@app.route('/grades/instructor/<string:instructor>', methods=['GET'])
def get_grades_by_instructor(instructor):
    """
    Get all grades assigned by a specific instructor
    ---
    tags:
      - Grades
    parameters:
      - name: instructor
        in: path
        type: string
        required: true
        description: Instructor name
    responses:
      200:
        description: List of grades for the instructor
        schema:
          type: array
          items:
            type: object
      404:
        description: No grades found for this instructor
    """
    start_time = time.time()
    log_request_details('👨‍🏫 GET GRADES BY INSTRUCTOR REQUEST', {'Instructor': instructor})

    try:
        log_db_operation('QUERY', {'table': 'grades', 'operation': 'SELECT BY INSTRUCTOR', 'instructor': instructor})
        grades = Grade.query.filter(Grade.instructor.isnot(None), Grade.instructor.ilike(instructor)).all()

        if not grades:
            execution_time = time.time() - start_time
            log_response_details(404, {'error': 'No grades found for this instructor'}, execution_time)
            return jsonify({'error': 'No grades found for this instructor'}), 404

        grades_data = [grade.to_dict() for grade in grades]
        execution_time = time.time() - start_time
        log_response_details(200, {'count': len(grades_data), 'grades': grades_data}, execution_time)
        return jsonify(grades_data), 200
    except Exception as e:
        log_error_details(e, {'operation': 'get_grades_by_instructor', 'instructor': instructor})
        return jsonify({'error': str(e)}), 500


# GET grade availability by enrollment ID
@app.route('/grades/availability/<int:enrollment_id>', methods=['GET'])
def check_grade_availability(enrollment_id):
    """
    Check whether grades are available for an enrollment
    ---
    tags:
      - Grades
    parameters:
      - name: enrollment_id
        in: path
        type: integer
        required: true
        description: The enrollment ID
    responses:
      200:
        description: Grade availability status
        schema:
          type: object
          properties:
            enrollment_id:
              type: integer
            grades_available:
              type: boolean
            total_records:
              type: integer
    """
    start_time = time.time()
    log_request_details('✅ CHECK GRADE AVAILABILITY REQUEST', {'Enrollment ID': enrollment_id})

    try:
        grades = Grade.query.filter_by(enrollment_id=enrollment_id).all()
        grades_with_values = [grade for grade in grades if grade.grade and grade.grade.strip()]

        response_data = {
            'enrollment_id': enrollment_id,
            'grades_available': len(grades_with_values) > 0,
            'total_records': len(grades),
            'graded_records': len(grades_with_values)
        }

        execution_time = time.time() - start_time
        log_response_details(200, response_data, execution_time)
        return jsonify(response_data), 200
    except Exception as e:
        log_error_details(e, {'operation': 'check_grade_availability', 'enrollment_id': enrollment_id})
        return jsonify({'error': str(e)}), 500

# POST create new grade
@app.route('/grades', methods=['POST'])
def create_grade():
    """
    Create a new grade
    ---
    tags:
      - Grades
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - enrollment_id
          properties:
            enrollment_id:
              type: integer
              example: 1
            instructor:
              type: string
              example: Dr. Silva
            grade:
              type: string
              example: A
            feedback:
              type: string
              example: Excellent performance
    responses:
      201:
        description: Grade created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Grade created successfully
            grade:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                enrollment_id:
                  type: integer
                  example: 1
                instructor:
                  type: string
                  example: Dr. Silva
                grade:
                  type: string
                  example: A
                feedback:
                  type: string
                  example: Excellent performance
                graded_at:
                  type: string
                  format: date-time
      400:
        description: Invalid input
      409:
        description: Duplicate grade for enrollment
    """
    start_time = time.time()
    data = request.get_json()
    log_request_details('➕ CREATE GRADE REQUEST', {'Request Body': data})
    
    try:
        if not data or 'enrollment_id' not in data:
            log_error_details(ValueError('Missing required field'), {'field': 'enrollment_id', 'provided_data': data})
            execution_time = time.time() - start_time
            log_response_details(400, {'error': 'enrollment_id is required'}, execution_time)
            return jsonify({'error': 'enrollment_id is required'}), 400

        # Business rule: one grade record per enrollment_id
        existing_grade = Grade.query.filter_by(enrollment_id=data['enrollment_id']).first()
        if existing_grade:
            response_data = {
                'error': 'Duplicate grade record for this enrollment_id',
                'enrollment_id': data['enrollment_id'],
                'existing_grade_id': existing_grade.id
            }
            execution_time = time.time() - start_time
            log_response_details(409, response_data, execution_time)
            return jsonify(response_data), 409
        
        log_db_operation('INSERT', {
            'table': 'grades',
            'data': {
                'enrollment_id': data['enrollment_id'],
                'instructor': data.get('instructor'),
                'grade': data.get('grade'),
                'feedback': data.get('feedback')
            }
        })
        
        new_grade = Grade(
            enrollment_id=data['enrollment_id'],
            instructor=data.get('instructor'),
            grade=data.get('grade'),
            feedback=data.get('feedback')
        )
        
        db.session.add(new_grade)
        db.session.commit()
        
        grade_data = new_grade.to_dict()
        log_db_operation('RESULT', {'success': True, 'inserted_id': new_grade.id, 'data': grade_data})
        
        execution_time = time.time() - start_time
        log_response_details(201, {'message': 'Grade created successfully', 'grade': grade_data}, execution_time)
        
        return jsonify({
            'message': 'Grade created successfully',
            'grade': grade_data
        }), 201
    except Exception as e:
        db.session.rollback()
        log_error_details(e, {'operation': 'create_grade', 'data': data})
        return jsonify({'error': str(e)}), 500

# PUT update grade
@app.route('/grades/<int:grade_id>', methods=['PUT'])
def update_grade(grade_id):
    """
    Update an existing grade
    ---
    tags:
      - Grades
    parameters:
      - name: grade_id
        in: path
        type: integer
        required: true
        description: The ID of the grade to update
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            enrollment_id:
              type: integer
              example: 1
            instructor:
              type: string
              example: Dr. Silva
            grade:
              type: string
              example: A
            feedback:
              type: string
              example: Excellent performance
    responses:
      200:
        description: Grade updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Grade updated successfully
            grade:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                enrollment_id:
                  type: integer
                  example: 1
                instructor:
                  type: string
                  example: Dr. Silva
                grade:
                  type: string
                  example: A
                feedback:
                  type: string
                  example: Excellent performance
                graded_at:
                  type: string
                  format: date-time
      404:
        description: Grade not found
      400:
        description: Invalid input
      409:
        description: Duplicate enrollment_id conflict
    """
    start_time = time.time()
    data = request.get_json()
    log_request_details('✏️ UPDATE GRADE REQUEST', {'Grade ID': grade_id, 'Request Body': data})
    
    try:
        log_db_operation('QUERY', {'table': 'grades', 'operation': 'SELECT BY ID', 'id': grade_id})
        grade = Grade.query.get(grade_id)
        
        if not grade:
            log_db_operation('RESULT', {'found': False, 'id': grade_id})
            execution_time = time.time() - start_time
            log_response_details(404, {'error': 'Grade not found'}, execution_time)
            return jsonify({'error': 'Grade not found'}), 404
        
        if not data:
            log_error_details(ValueError('No data provided'), {'grade_id': grade_id})
            execution_time = time.time() - start_time
            log_response_details(400, {'error': 'No data provided'}, execution_time)
            return jsonify({'error': 'No data provided'}), 400

        if 'enrollment_id' in data:
            duplicate_grade = Grade.query.filter(
                Grade.enrollment_id == data['enrollment_id'],
                Grade.id != grade_id
            ).first()
            if duplicate_grade:
                response_data = {
                    'error': 'Duplicate grade record for this enrollment_id',
                    'enrollment_id': data['enrollment_id'],
                    'conflicting_grade_id': duplicate_grade.id
                }
                execution_time = time.time() - start_time
                log_response_details(409, response_data, execution_time)
                return jsonify(response_data), 409
        
        # Track changes
        changes = {}
        if 'enrollment_id' in data and data['enrollment_id'] != grade.enrollment_id:
            changes['enrollment_id'] = {'old': grade.enrollment_id, 'new': data['enrollment_id']}
            grade.enrollment_id = data['enrollment_id']
        if 'instructor' in data and data['instructor'] != grade.instructor:
            changes['instructor'] = {'old': grade.instructor, 'new': data['instructor']}
            grade.instructor = data['instructor']
        if 'grade' in data and data['grade'] != grade.grade:
            changes['grade'] = {'old': grade.grade, 'new': data['grade']}
            grade.grade = data['grade']
        if 'feedback' in data and data['feedback'] != grade.feedback:
            changes['feedback'] = {'old': grade.feedback, 'new': data['feedback']}
            grade.feedback = data['feedback']
        
        log_db_operation('UPDATE', {
            'table': 'grades',
            'id': grade_id,
            'changes': changes
        })
        
        db.session.commit()
        
        grade_data = grade.to_dict()
        log_db_operation('RESULT', {'success': True, 'updated_id': grade_id, 'data': grade_data})
        
        execution_time = time.time() - start_time
        log_response_details(200, {'message': 'Grade updated successfully', 'grade': grade_data}, execution_time)
        
        return jsonify({
            'message': 'Grade updated successfully',
            'grade': grade_data
        }), 200
    except Exception as e:
        db.session.rollback()
        log_error_details(e, {'operation': 'update_grade', 'grade_id': grade_id, 'data': data})
        return jsonify({'error': str(e)}), 500

# DELETE grade
@app.route('/grades/<int:grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    """
    Delete a grade
    ---
    tags:
      - Grades
    parameters:
      - name: grade_id
        in: path
        type: integer
        required: true
        description: The ID of the grade to delete
    responses:
      200:
        description: Grade deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Grade deleted successfully
      404:
        description: Grade not found
    """
    start_time = time.time()
    log_request_details('🗑️ DELETE GRADE REQUEST', {'Grade ID': grade_id})
    
    try:
        log_db_operation('QUERY', {'table': 'grades', 'operation': 'SELECT BY ID', 'id': grade_id})
        grade = Grade.query.get(grade_id)
        
        if not grade:
            log_db_operation('RESULT', {'found': False, 'id': grade_id})
            execution_time = time.time() - start_time
            log_response_details(404, {'error': 'Grade not found'}, execution_time)
            return jsonify({'error': 'Grade not found'}), 404
        
        grade_data = grade.to_dict()
        log_db_operation('DELETE', {'table': 'grades', 'id': grade_id, 'data': grade_data})
        
        db.session.delete(grade)
        db.session.commit()
        
        log_db_operation('RESULT', {'success': True, 'deleted_id': grade_id})
        
        execution_time = time.time() - start_time
        log_response_details(200, {'message': 'Grade deleted successfully'}, execution_time)
        
        return jsonify({'message': 'Grade deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        log_error_details(e, {'operation': 'delete_grade', 'grade_id': grade_id})
        return jsonify({'error': str(e)}), 500

# Helper function to convert letter grade to grade points
def grade_to_points(grade):
    """Convert letter grade to grade points."""
    grade_map = {
        'A+': 4.0,
        'A': 4.0,
        'A-': 3.7,
        'B+': 3.3,
        'B': 3.0,
        'B-': 2.7,
        'C+': 2.3,
        'C': 2.0,
        'C-': 1.7,
        'D+': 1.3,
        'D': 1.0,
        'D-': 0.7,
        'F': 0.0
    }
    return grade_map.get(grade.upper(), 0.0)

# Calculate GPA for a student
@app.route('/grades/gpa/<int:enrollment_id>', methods=['GET'])
def calculate_gpa(enrollment_id):
    """
    Calculate GPA for a specific enrollment
    ---
    tags:
      - Grades
    parameters:
      - name: enrollment_id
        in: path
        type: integer
        required: true
        description: The enrollment ID
    responses:
      200:
        description: GPA calculation result
        schema:
          type: object
          properties:
            enrollment_id:
              type: integer
              example: 1
            total_grades:
              type: integer
              example: 5
            total_grade_points:
              type: number
              example: 18.5
            gpa:
              type: number
              example: 3.7
            grades_breakdown:
              type: array
              items:
                type: object
                properties:
                  grade:
                    type: string
                    example: A
                  grade_points:
                    type: number
                    example: 4.0
      404:
        description: No grades found for this enrollment
    """
    start_time = time.time()
    log_request_details('📊 CALCULATE GPA REQUEST', {'Enrollment ID': enrollment_id})
    
    try:
        log_db_operation('QUERY', {'table': 'grades', 'operation': 'SELECT BY ENROLLMENT ID', 'enrollment_id': enrollment_id})
        grades = Grade.query.filter_by(enrollment_id=enrollment_id).all()
        
        if not grades:
            log_db_operation('RESULT', {'found': False, 'enrollment_id': enrollment_id})
            execution_time = time.time() - start_time
            log_response_details(404, {'error': 'No grades found for this enrollment'}, execution_time)
            return jsonify({'error': 'No grades found for this enrollment'}), 404
        
        total_grade_points = 0.0
        grades_breakdown = []
        
        for grade in grades:
            if grade.grade:
                points = grade_to_points(grade.grade)
                total_grade_points += points
                grades_breakdown.append({
                    'grade': grade.grade,
                    'grade_points': points
                })
        
        total_grades = len(grades_breakdown)
        gpa = total_grade_points / total_grades if total_grades > 0 else 0.0
        
        response_data = {
            'enrollment_id': enrollment_id,
            'total_grades': total_grades,
            'total_grade_points': round(total_grade_points, 2),
            'gpa': round(gpa, 2),
            'grades_breakdown': grades_breakdown
        }
        
        log_db_operation('RESULT', {
            'found': True,
            'enrollment_id': enrollment_id,
            'total_grades': total_grades,
            'gpa': round(gpa, 2)
        })
        
        execution_time = time.time() - start_time
        log_response_details(200, response_data, execution_time)
        
        return jsonify(response_data), 200
    except Exception as e:
        log_error_details(e, {'operation': 'calculate_gpa', 'enrollment_id': enrollment_id})
        return jsonify({'error': str(e)}), 500

# Calculate overall GPA across all enrollments
@app.route('/grades/gpa/overall', methods=['GET'])
def calculate_overall_gpa():
    """
    Calculate overall GPA across all enrollments
    ---
    tags:
      - Grades
    responses:
      200:
        description: Overall GPA calculation result
        schema:
          type: object
          properties:
            total_grades:
              type: integer
              example: 10
            total_grade_points:
              type: number
              example: 35.5
            overall_gpa:
              type: number
              example: 3.55
            enrollments_count:
              type: integer
              example: 3
      404:
        description: No grades found
    """
    start_time = time.time()
    log_request_details('📈 CALCULATE OVERALL GPA REQUEST')
    
    try:
        log_db_operation('QUERY', {'table': 'grades', 'operation': 'SELECT ALL'})
        grades = Grade.query.all()
        
        if not grades:
            log_db_operation('RESULT', {'found': False})
            execution_time = time.time() - start_time
            log_response_details(404, {'error': 'No grades found'}, execution_time)
            return jsonify({'error': 'No grades found'}), 404
        
        total_grade_points = 0.0
        total_grades = 0
        enrollment_ids = set()
        
        for grade in grades:
            if grade.grade:
                points = grade_to_points(grade.grade)
                total_grade_points += points
                total_grades += 1
                enrollment_ids.add(grade.enrollment_id)
        
        overall_gpa = total_grade_points / total_grades if total_grades > 0 else 0.0
        
        response_data = {
            'total_grades': total_grades,
            'total_grade_points': round(total_grade_points, 2),
            'overall_gpa': round(overall_gpa, 2),
            'enrollments_count': len(enrollment_ids)
        }
        
        log_db_operation('RESULT', {
            'found': True,
            'total_grades': total_grades,
            'overall_gpa': round(overall_gpa, 2),
            'enrollments_count': len(enrollment_ids)
        })
        
        execution_time = time.time() - start_time
        log_response_details(200, response_data, execution_time)
        
        return jsonify(response_data), 200
    except Exception as e:
        log_error_details(e, {'operation': 'calculate_overall_gpa'})
        return jsonify({'error': str(e)}), 500


@app.route('/api-docs', methods=['GET'])
def legacy_swagger_redirect():
    """Keep backward compatibility for older Swagger URL."""
    return redirect('/apidocs', code=302)


if __name__ == '__main__':
    logger.info('╔' + '═' * 78 + '╗')
    logger.info(f'║ {"GRADE SERVICE STARTING":^78} ║')
    logger.info('╠' + '═' * 78 + '╣')
    logger.info(f'║ 🚀 Server: http://0.0.0.0:5004{"":<48} ║')
    logger.info(f'║ 📚 Swagger UI: http://localhost:5004/apidocs{"":<35} ║')
    logger.info(f'║ 🗄️  Database: SQLite (grade_service.db){"":<39} ║')
    logger.info(f'║ 📅 Started: {datetime.now().isoformat():<64} ║')
    logger.info('╚' + '═' * 78 + '╝')
    log_api_endpoints()
    app.run(host='0.0.0.0', port=5004, debug=True)
