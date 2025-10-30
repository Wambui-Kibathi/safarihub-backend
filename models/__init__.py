from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .destination import Destination
from .payment import Payment

__all__ = ['db', 'User', 'Destination', 'Payment']