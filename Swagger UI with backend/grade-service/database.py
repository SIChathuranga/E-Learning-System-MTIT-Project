from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grade_service.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        _migrate_grades_table()


def _migrate_grades_table():
    """Apply lightweight schema upgrades for existing SQLite databases."""
    columns = db.session.execute(text("PRAGMA table_info(grades)")).fetchall()
    existing_columns = {column[1] for column in columns}

    if 'instructor' not in existing_columns:
        db.session.execute(text("ALTER TABLE grades ADD COLUMN instructor VARCHAR(100)"))
        db.session.commit()
