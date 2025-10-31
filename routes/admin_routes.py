from flask import Blueprint, jsonify
from utils.jwt_service import token_required, role_required
from utils.db import db
from models.user import User
from models.booking import Booking
from models.payment import Payment

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/dashboard", methods=["GET"])
@token_required
@role_required("admin")
def admin_dashboard(current_user):
    """Get admin dashboard statistics"""
    try:
        total_users = User.query.count()
        total_bookings = Booking.query.count()
        total_payments = Payment.query.filter_by(status='completed').count()
        total_revenue = db.session.query(db.func.sum(Payment.amount)).filter(Payment.status == 'completed').scalar() or 0

        return jsonify({
            "total_users": total_users,
            "total_bookings": total_bookings,
            "total_payments": total_payments,
            "total_revenue": total_revenue
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/users", methods=["GET"])
@token_required
@role_required("admin")
def get_all_users(current_user):
    """Get all users (admin only)"""
    try:
        users = User.query.all()
        users_data = [{
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat() if user.created_at else None
        } for user in users]

        return jsonify({"users": users_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/bookings", methods=["GET"])
@token_required
@role_required("admin")
def get_all_bookings(current_user):
    """Get all bookings (admin only)"""
    try:
        bookings = Booking.query.all()
        bookings_data = [{
            "id": booking.id,
            "user_id": booking.user_id,
            "destination_id": booking.destination_id,
            "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
            "travel_date": booking.travel_date.isoformat() if booking.travel_date else None,
            "number_of_people": booking.number_of_people,
            "total_amount": booking.total_amount,
            "status": booking.status
        } for booking in bookings]

        return jsonify({"bookings": bookings_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
