"""Database models for the Flask application."""

from sqlalchemy.sql import func

from flask_app.core import db


class BaseModel(db.Model):
    """Base model class that includes common fields."""

    __abstract__ = True

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class Example(BaseModel):
    """Example model to demonstrate SQLAlchemy usage."""

    __tablename__ = "examples"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        """String representation of the Example model. Helpful for debugging.

        Returns:
            str: String representation including the example name.
        """
        return f"<Example {self.name}>"
