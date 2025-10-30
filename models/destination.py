from datetime import datetime
from . import db

class Destination(db.Model):
    __tablename__ = 'destinations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    location = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    price_per_day = db.Column(db.Float, nullable=False)
    max_capacity = db.Column(db.Integer, default=10)
    image_url = db.Column(db.String(255))
    duration_days = db.Column(db.Integer, default=1)
    difficulty_level = db.Column(db.String(20), default='easy')  # easy, moderate, hard
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def is_available(self):
        return self.is_active

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'price_per_day': self.price_per_day,
            'max_capacity': self.max_capacity,
            'image_url': self.image_url,
            'duration_days': self.duration_days,
            'difficulty_level': self.difficulty_level,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def total_price(self):
        return self.price_per_day * self.duration_days
    
    def __repr__(self):
        return f'<Destination {self.name}>'