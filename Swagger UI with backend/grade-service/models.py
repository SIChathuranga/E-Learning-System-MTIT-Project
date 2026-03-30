from database import db
from datetime import datetime

class Grade(db.Model):
    """Grade model for storing grade information."""
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enrollment_id = db.Column(db.Integer, nullable=False)
    instructor = db.Column(db.String(100), nullable=True)
    grade = db.Column(db.String(5), nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    graded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert grade object to dictionary."""
        return {
            'id': self.id,
            'enrollment_id': self.enrollment_id,
            'instructor': self.instructor,
            'grade': self.grade,
            'feedback': self.feedback,
            'graded_at': self.graded_at.isoformat() if self.graded_at else None
        }
    
    def __repr__(self):
        return f'<Grade {self.id}: {self.grade}>'
