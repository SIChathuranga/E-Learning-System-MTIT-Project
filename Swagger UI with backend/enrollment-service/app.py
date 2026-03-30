from __future__ import annotations

from copy import deepcopy
from datetime import date
from typing import Any

from flask import Flask, jsonify, redirect, request

try:
    from flask_cors import CORS
except ModuleNotFoundError:
    CORS = None

app = Flask(__name__)

if CORS is not None:
    CORS(app)


ALLOWED_STATUSES = {"active", "completed", "dropped"}
SEED_ENROLLMENTS = [
    {
        "id": 1,
        "studentId": 101,
        "courseId": 201,
        "enrolledDate": "2026-03-28",
        "status": "active",
    },
    {
        "id": 2,
        "studentId": 102,
        "courseId": 202,
        "enrolledDate": "2026-03-28",
        "status": "completed",
    },
]

enrollments = deepcopy(SEED_ENROLLMENTS)
next_id = max(item["id"] for item in enrollments) + 1


OPENAPI_SPEC: dict[str, Any] = {
    "openapi": "3.0.3",
    "info": {
        "title": "Enrollment Service API",
        "version": "1.0.0",
        "description": (
            "Microservice for managing student-course enrollment relationships "
            "in the E-Learning platform."
        ),
    },
    "servers": [
        {"url": "http://localhost:5003", "description": "Direct access"},
        {
            "url": "http://localhost:8080/enrollment-service",
            "description": "Via API Gateway",
        },
    ],
    "tags": [
        {"name": "Health", "description": "Operational status"},
        {"name": "Enrollments", "description": "Enrollment lifecycle management"},
        {"name": "Relationships", "description": "Student-course mapping queries"},
    ],
    "paths": {
        "/health": {
            "get": {
                "tags": ["Health"],
                "summary": "Health check",
                "responses": {
                    "200": {
                        "description": "Service is running",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/HealthResponse"}
                            }
                        },
                    }
                },
            }
        },
        "/enrollments": {
            "get": {
                "tags": ["Enrollments"],
                "summary": "Get all enrollments",
                "responses": {
                    "200": {
                        "description": "Enrollment list",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Enrollment"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Enrollments"],
                "summary": "Create or reactivate an enrollment",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/CreateEnrollmentRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Dropped enrollment reactivated",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Enrollment"}
                            }
                        },
                    },
                    "201": {
                        "description": "Enrollment created",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Enrollment"}
                            }
                        },
                    },
                    "400": {
                        "description": "Missing or invalid fields",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        },
                    },
                    "409": {
                        "description": "Duplicate active/completed enrollment",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        },
                    },
                },
            },
        },
        "/enrollments/{enrollmentId}": {
            "get": {
                "tags": ["Enrollments"],
                "summary": "Get enrollment by ID",
                "parameters": [
                    {
                        "name": "enrollmentId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Enrollment details",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Enrollment"}
                            }
                        },
                    },
                    "404": {
                        "description": "Enrollment not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        },
                    },
                },
            },
            "put": {
                "tags": ["Enrollments"],
                "summary": "Update enrollment status",
                "parameters": [
                    {
                        "name": "enrollmentId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UpdateEnrollmentRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Enrollment updated",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Enrollment"}
                            }
                        },
                    },
                    "400": {
                        "description": "Missing or invalid status",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        },
                    },
                    "404": {
                        "description": "Enrollment not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        },
                    },
                },
            },
            "delete": {
                "tags": ["Enrollments"],
                "summary": "Soft-drop an enrollment",
                "parameters": [
                    {
                        "name": "enrollmentId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Enrollment dropped",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Enrollment"}
                            }
                        },
                    },
                    "404": {
                        "description": "Enrollment not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        },
                    },
                },
            },
        },
        "/students/{studentId}/courses": {
            "get": {
                "tags": ["Relationships"],
                "summary": "Get enrollment records for one student",
                "parameters": [
                    {
                        "name": "studentId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Student enrollment records",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Enrollment"},
                                }
                            }
                        },
                    }
                },
            }
        },
        "/courses/{courseId}/students": {
            "get": {
                "tags": ["Relationships"],
                "summary": "Get enrollment records for one course",
                "parameters": [
                    {
                        "name": "courseId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Course enrollment records",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Enrollment"},
                                }
                            }
                        },
                    }
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Enrollment": {
                "type": "object",
                "required": ["id", "studentId", "courseId", "enrolledDate", "status"],
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "studentId": {"type": "integer", "example": 101},
                    "courseId": {"type": "integer", "example": 201},
                    "enrolledDate": {
                        "type": "string",
                        "format": "date",
                        "example": "2026-03-28",
                    },
                    "status": {
                        "type": "string",
                        "enum": sorted(ALLOWED_STATUSES),
                        "example": "active",
                    },
                },
            },
            "CreateEnrollmentRequest": {
                "type": "object",
                "required": ["studentId", "courseId"],
                "properties": {
                    "studentId": {"type": "integer", "example": 101},
                    "courseId": {"type": "integer", "example": 201},
                },
            },
            "UpdateEnrollmentRequest": {
                "type": "object",
                "required": ["status"],
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": sorted(ALLOWED_STATUSES),
                        "example": "completed",
                    }
                },
            },
            "HealthResponse": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "example": "OK"},
                    "service": {"type": "string", "example": "Enrollment Service"},
                    "docs": {"type": "string", "example": "/api-docs/"},
                },
            },
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Student already enrolled in this course",
                    }
                },
            },
        }
    },
}


@app.after_request
def add_cors_headers(response):
    if CORS is None:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


@app.route("/api-docs")
def api_docs_redirect():
    return redirect("/api-docs/")


@app.route("/openapi.json")
def openapi_json():
    return jsonify(OPENAPI_SPEC)


@app.route("/api-docs/")
def api_docs():
    return """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Enrollment Service API Docs</title>
    <link
      rel="stylesheet"
      href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"
    />
    <style>
      body { margin: 0; background: #f3f4f6; }
      .topbar { display: none; }
      .swagger-ui .scheme-container { box-shadow: none; }
    </style>
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      window.onload = () => {
        window.ui = SwaggerUIBundle({
          url: "../openapi.json",
          dom_id: "#swagger-ui",
          deepLinking: true,
          displayRequestDuration: true,
          presets: [SwaggerUIBundle.presets.apis]
        });
      };
    </script>
  </body>
</html>
"""


def today_string() -> str:
    return date.today().isoformat()


def error_response(message: str, status_code: int):
    return jsonify({"error": message}), status_code


def find_enrollment(enrollment_id: int) -> dict[str, Any] | None:
    return next((item for item in enrollments if item["id"] == enrollment_id), None)


def is_valid_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def parse_json_body() -> dict[str, Any] | None:
    return request.get_json(silent=True)


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint for the Enrollment Service.
    """
    return jsonify({"status": "OK", "service": "Enrollment Service", "docs": "/api-docs/"})


@app.route("/enrollments", methods=["GET"])
def get_enrollments():
    """
    Return all enrollment records, including dropped records.
    """
    return jsonify(enrollments)


@app.route("/enrollments/<int:enrollment_id>", methods=["GET"])
def get_enrollment(enrollment_id: int):
    """
    Return a single enrollment by its identifier.
    """
    enrollment = find_enrollment(enrollment_id)
    if enrollment is None:
        return error_response("Enrollment not found", 404)
    return jsonify(enrollment)


@app.route("/enrollments", methods=["POST"])
def create_enrollment():
    """
    Create a new enrollment or reactivate a dropped enrollment.
    """
    global next_id

    payload = parse_json_body()
    if payload is None:
        return error_response("Request body must be valid JSON", 400)

    student_id = payload.get("studentId")
    course_id = payload.get("courseId")

    if student_id is None or course_id is None:
        return error_response("studentId and courseId are required", 400)
    if not is_valid_int(student_id) or not is_valid_int(course_id):
        return error_response("studentId and courseId must be integers", 400)

    for enrollment in enrollments:
        if enrollment["studentId"] == student_id and enrollment["courseId"] == course_id:
            if enrollment["status"] == "dropped":
                enrollment["status"] = "active"
                enrollment["enrolledDate"] = today_string()
                return jsonify(enrollment), 200
            return error_response("Student already enrolled in this course", 409)

    new_enrollment = {
        "id": next_id,
        "studentId": student_id,
        "courseId": course_id,
        "enrolledDate": today_string(),
        "status": "active",
    }
    enrollments.append(new_enrollment)
    next_id += 1
    return jsonify(new_enrollment), 201


@app.route("/enrollments/<int:enrollment_id>", methods=["PUT"])
def update_enrollment(enrollment_id: int):
    """
    Update the status of an enrollment.
    """
    enrollment = find_enrollment(enrollment_id)
    if enrollment is None:
        return error_response("Enrollment not found", 404)

    payload = parse_json_body()
    if payload is None:
        return error_response("Request body must be valid JSON", 400)

    status = payload.get("status")
    if status is None:
        return error_response("status is required", 400)
    if status not in ALLOWED_STATUSES:
        return error_response(
            "status must be one of active, completed, or dropped",
            400,
        )

    enrollment["status"] = status
    return jsonify(enrollment)


@app.route("/enrollments/<int:enrollment_id>", methods=["DELETE"])
def drop_enrollment(enrollment_id: int):
    """
    Soft-drop an enrollment by marking it as dropped.
    """
    enrollment = find_enrollment(enrollment_id)
    if enrollment is None:
        return error_response("Enrollment not found", 404)

    enrollment["status"] = "dropped"
    return jsonify(enrollment)


@app.route("/students/<int:student_id>/courses", methods=["GET"])
def get_courses_by_student(student_id: int):
    """
    Return all enrollment records for a student.
    """
    student_enrollments = [
        item for item in enrollments if item["studentId"] == student_id
    ]
    return jsonify(student_enrollments)


@app.route("/courses/<int:course_id>/students", methods=["GET"])
def get_students_by_course(course_id: int):
    """
    Return all enrollment records for a course.
    """
    course_enrollments = [
        item for item in enrollments if item["courseId"] == course_id
    ]
    return jsonify(course_enrollments)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False)
