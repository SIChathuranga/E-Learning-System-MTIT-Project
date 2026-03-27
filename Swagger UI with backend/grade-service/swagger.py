swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Grade Service API",
        "description": "API for managing grades in the E-Learning System",
        "version": "1.0.0",
        "contact": {
            "name": "Grade Service Team",
            "email": "grade@example.com"
        }
    },
    "basePath": "/",
    "schemes": ["http"],
    "tags": [
        {
            "name": "Grades",
            "description": "Operations for managing grades"
        },
        {
            "name": "Health",
            "description": "Health check operations"
        }
    ]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs"
}
