const express = require('express');
const cors = require('cors');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');

const app = express();
const PORT = 5002;

// ========== MIDDLEWARE ==========
app.use(cors());
app.use(express.json());

// ========== IN-MEMORY DATABASE ==========
let courses = [
    {
        id: 1,
        name: "Introduction to Programming",
        code: "CS101",
        credits: 3,
        instructor: "Dr. Smith",
        description: "Learn fundamental programming concepts using Python",
        capacity: 30,
        enrolled: 25
    },
    {
        id: 2,
        name: "Web Development Fundamentals",
        code: "CS201",
        credits: 3,
        instructor: "Prof. Johnson",
        description: "Build modern websites with HTML, CSS, and JavaScript",
        capacity: 25,
        enrolled: 22
    }
];

let nextId = 3;

// ========== HELPER FUNCTIONS ==========
const findCourseById = (id) => {
    return courses.find(course => course.id === id);
};

const findCourseIndex = (id) => {
    return courses.findIndex(course => course.id === id);
};

// ========== API ENDPOINTS ==========

/**
 * @swagger
 * components:
 *   schemas:
 *     Course:
 *       type: object
 *       required:
 *         - name
 *         - code
 *       properties:
 *         id:
 *           type: integer
 *           description: The auto-generated id of the course
 *         name:
 *           type: string
 *           description: Course name
 *         code:
 *           type: string
 *           description: Course code (must be unique)
 *         credits:
 *           type: integer
 *           description: Number of credits for the course
 *         instructor:
 *           type: string
 *           description: Name of the instructor
 *         description:
 *           type: string
 *           description: Course description
 *         capacity:
 *           type: integer
 *           description: Maximum number of students
 *         enrolled:
 *           type: integer
 *           description: Current number of enrolled students
 *       example:
 *         id: 1
 *         name: Introduction to Programming
 *         code: CS101
 *         credits: 3
 *         instructor: Dr. Smith
 *         description: Learn fundamental programming concepts
 *         capacity: 30
 *         enrolled: 25
 */

/**
 * @swagger
 * /courses:
 *   get:
 *     summary: Retrieve all courses
 *     tags: [Courses]
 *     responses:
 *       200:
 *         description: List of all courses
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 count:
 *                   type: integer
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/Course'
 */
app.get('/courses', (req, res) => {
    res.status(200).json({
        success: true,
        count: courses.length,
        data: courses
    });
});

/**
 * @swagger
 * /courses/{id}:
 *   get:
 *     summary: Get a course by ID
 *     tags: [Courses]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: Course ID
 *     responses:
 *       200:
 *         description: Course details
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   $ref: '#/components/schemas/Course'
 *       404:
 *         description: Course not found
 */
app.get('/courses/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const course = findCourseById(id);
    
    if (!course) {
        return res.status(404).json({
            success: false,
            error: `Course with ID ${id} not found`
        });
    }
    
    res.status(200).json({
        success: true,
        data: course
    });
});

/**
 * @swagger
 * /courses:
 *   post:
 *     summary: Create a new course
 *     tags: [Courses]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - name
 *               - code
 *             properties:
 *               name:
 *                 type: string
 *               code:
 *                 type: string
 *               credits:
 *                 type: integer
 *               instructor:
 *                 type: string
 *               description:
 *                 type: string
 *               capacity:
 *                 type: integer
 *     responses:
 *       201:
 *         description: Course created successfully
 *       400:
 *         description: Invalid input or duplicate course code
 */
app.post('/courses', (req, res) => {
    const { name, code, credits, instructor, description, capacity } = req.body;
    
    // Validate required fields
    if (!name || !code) {
        return res.status(400).json({
            success: false,
            error: 'Name and course code are required fields'
        });
    }
    
    // Check for duplicate course code
    const existingCourse = courses.find(course => course.code === code);
    if (existingCourse) {
        return res.status(400).json({
            success: false,
            error: `Course with code ${code} already exists`
        });
    }
    
    // Create new course
    const newCourse = {
        id: nextId++,
        name: name,
        code: code,
        credits: credits || 3,
        instructor: instructor || 'TBA',
        description: description || 'No description available',
        capacity: capacity || 30,
        enrolled: 0
    };
    
    courses.push(newCourse);
    
    res.status(201).json({
        success: true,
        data: newCourse,
        message: 'Course created successfully'
    });
});

/**
 * @swagger
 * /courses/{id}:
 *   put:
 *     summary: Update a course completely
 *     tags: [Courses]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: Course ID
 *     requestBody:
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *               code:
 *                 type: string
 *               credits:
 *                 type: integer
 *               instructor:
 *                 type: string
 *               description:
 *                 type: string
 *               capacity:
 *                 type: integer
 *     responses:
 *       200:
 *         description: Course updated successfully
 *       404:
 *         description: Course not found
 */
app.put('/courses/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const index = findCourseIndex(id);
    
    if (index === -1) {
        return res.status(404).json({
            success: false,
            error: `Course with ID ${id} not found`
        });
    }
    
    // Update course with new data (keep existing values if not provided)
    const updatedCourse = {
        ...courses[index],
        name: req.body.name || courses[index].name,
        code: req.body.code || courses[index].code,
        credits: req.body.credits || courses[index].credits,
        instructor: req.body.instructor || courses[index].instructor,
        description: req.body.description || courses[index].description,
        capacity: req.body.capacity || courses[index].capacity
    };
    
    courses[index] = updatedCourse;
    
    res.status(200).json({
        success: true,
        data: updatedCourse,
        message: 'Course updated successfully'
    });
});

/**
 * @swagger
 * /courses/{id}:
 *   patch:
 *     summary: Partially update a course
 *     tags: [Courses]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: Course ID
 *     requestBody:
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *               code:
 *                 type: string
 *               credits:
 *                 type: integer
 *               instructor:
 *                 type: string
 *               description:
 *                 type: string
 *               capacity:
 *                 type: integer
 *     responses:
 *       200:
 *         description: Course partially updated successfully
 *       404:
 *         description: Course not found
 */
app.patch('/courses/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const index = findCourseIndex(id);
    
    if (index === -1) {
        return res.status(404).json({
            success: false,
            error: `Course with ID ${id} not found`
        });
    }
    
    // Only update fields that are provided in the request
    const allowedUpdates = ['name', 'code', 'credits', 'instructor', 'description', 'capacity'];
    const updates = {};
    
    allowedUpdates.forEach(field => {
        if (req.body[field] !== undefined) {
            updates[field] = req.body[field];
        }
    });
    
    courses[index] = {
        ...courses[index],
        ...updates
    };
    
    res.status(200).json({
        success: true,
        data: courses[index],
        message: 'Course partially updated successfully'
    });
});

/**
 * @swagger
 * /courses/{id}:
 *   delete:
 *     summary: Delete a course
 *     tags: [Courses]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: Course ID
 *     responses:
 *       200:
 *         description: Course deleted successfully
 *       400:
 *         description: Cannot delete course with enrolled students
 *       404:
 *         description: Course not found
 */
app.delete('/courses/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const index = findCourseIndex(id);
    
    if (index === -1) {
        return res.status(404).json({
            success: false,
            error: `Course with ID ${id} not found`
        });
    }
    
    // Check if course has enrolled students
    const course = courses[index];
    if (course.enrolled > 0) {
        return res.status(400).json({
            success: false,
            error: `Cannot delete course with ${course.enrolled} enrolled students. Drop all students first.`
        });
    }
    
    const deletedCourse = courses.splice(index, 1);
    
    res.status(200).json({
        success: true,
        data: deletedCourse[0],
        message: 'Course deleted successfully'
    });
});

/**
 * @swagger
 * /courses/instructor/{instructor}:
 *   get:
 *     summary: Get courses by instructor name
 *     tags: [Courses]
 *     parameters:
 *       - in: path
 *         name: instructor
 *         required: true
 *         schema:
 *           type: string
 *         description: Instructor name
 *     responses:
 *       200:
 *         description: List of courses taught by the instructor
 */
app.get('/courses/instructor/:instructor', (req, res) => {
    const instructor = req.params.instructor;
    const filteredCourses = courses.filter(
        course => course.instructor.toLowerCase().includes(instructor.toLowerCase())
    );
    
    res.status(200).json({
        success: true,
        count: filteredCourses.length,
        data: filteredCourses
    });
});

/**
 * @swagger
 * /courses/available:
 *   get:
 *     summary: Get courses with available seats
 *     tags: [Courses]
 *     responses:
 *       200:
 *         description: List of courses that have available seats
 */
app.get('/courses/available', (req, res) => {
    const availableCourses = courses.filter(
        course => course.enrolled < course.capacity
    );
    
    res.status(200).json({
        success: true,
        count: availableCourses.length,
        data: availableCourses
    });
});

/**
 * @swagger
 * /stats:
 *   get:
 *     summary: Get course statistics
 *     tags: [Statistics]
 *     responses:
 *       200:
 *         description: Course statistics
 */
app.get('/stats', (req, res) => {
    const totalCourses = courses.length;
    const totalEnrolled = courses.reduce((sum, course) => sum + course.enrolled, 0);
    const totalCapacity = courses.reduce((sum, course) => sum + course.capacity, 0);
    const averageEnrollment = totalCourses > 0 ? (totalEnrolled / totalCourses).toFixed(2) : 0;
    
    res.status(200).json({
        success: true,
        data: {
            totalCourses,
            totalEnrolled,
            totalCapacity,
            averageEnrollment: parseFloat(averageEnrollment),
            utilizationRate: totalCapacity > 0 ? ((totalEnrolled / totalCapacity) * 100).toFixed(2) + '%' : '0%'
        }
    });
});

// ========== SWAGGER CONFIGURATION ==========
const swaggerOptions = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'Course Service API',
            version: '1.0.0',
            description: 'Complete API for managing courses in the E-Learning Platform',
            contact: {
                name: 'Your Name',
                email: 'your.email@example.com'
            },
            license: {
                name: 'MIT',
                url: 'https://opensource.org/licenses/MIT'
            }
        },
        servers: [
            {
                url: `http://localhost:${PORT}`,
                description: 'Direct access to Course Service'
            },
            {
                url: 'http://localhost:8080/course-service',
                description: 'Access via API Gateway'
            }
        ],
        tags: [
            {
                name: 'Courses',
                description: 'Course management operations'
            },
            {
                name: 'Statistics',
                description: 'Course statistics and analytics'
            }
        ]
    },
    apis: ['./app.js']
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// ========== START SERVER ==========
app.listen(PORT, () => {
    console.log('========================================');
    console.log('✅ Course Service is running!');
    console.log('========================================');
    console.log(`📚 Direct Access: http://localhost:${PORT}`);
    console.log(`📖 Swagger UI: http://localhost:${PORT}/api-docs`);
    console.log(`🎯 API Endpoint: http://localhost:${PORT}/courses`);
    console.log('========================================');
    console.log('Available Endpoints:');
    console.log(`  GET    /courses                    - Get all courses`);
    console.log(`  GET    /courses/:id                - Get course by ID`);
    console.log(`  POST   /courses                    - Create new course`);
    console.log(`  PUT    /courses/:id                - Update course`);
    console.log(`  PATCH  /courses/:id                - Partially update course`);
    console.log(`  DELETE /courses/:id                - Delete course`);
    console.log(`  GET    /courses/instructor/:name   - Get courses by instructor`);
    console.log(`  GET    /courses/available          - Get courses with seats`);
    console.log(`  GET    /stats                      - Get course statistics`);
    console.log('========================================');
});