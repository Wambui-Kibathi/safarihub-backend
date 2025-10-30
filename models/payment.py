from datetime import datetime
from . import db

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_method = db.Column(db.String(20), nullable=False, index=True)  # stripe, mpesa
    transaction_id = db.Column(db.String(100), unique=True, index=True)
    status = db.Column(db.String(20), default='pending', index=True)  # pending, completed, failed, refunded
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    destination = db.relationship('Destination', backref='payments', lazy=True)
    
    @property
    def formatted_amount(self):
        return f"{self.currency} {self.amount:.2f}"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'destination_id': self.destination_id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def is_successful(self):
        return self.status == 'completed'
    
    def is_pending(self):
        return self.status == 'pending'
    
    def __repr__(self):
        return f'<Payment {self.transaction_id}>'