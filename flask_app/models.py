from sqlalchemy.sql import func
from flask_app.core import db

class BaseModel(db.Model):
    """Base model class that includes common fields and methods"""
    __abstract__ = True

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        """Convert model to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Example(BaseModel):
    """Example model to demonstrate SQLAlchemy usage"""
    __tablename__ = 'examples'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Example {self.name}>'
