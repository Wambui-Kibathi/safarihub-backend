from flask import Blueprint, request, jsonify
from utils.db import db
from models.user import User, GuideProfile
from models.destination import Trip, Destination
from models.payment import Booking, Payment
from utils.jwt_service import token_required, role_required
from utils.helpers import success_response, error_response, paginate_query
from sqlalchemy import func

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@token_required
@role_required(['admin'])
def get_admin_dashboard():
    # Get overall statistics
    total_users = User.query.count()
    total_guides = User.query.filter_by(role='guide').count()
    total_travelers = User.query.filter_by(role='traveler').count()
    total_trips = Trip.query.count()
    active_trips = Trip.query.filter_by(is_active=True).count()
    total_bookings = Booking.query.count()
    total_revenue = db.session.query(func.sum(Payment.amount)).filter_by(payment_status='completed').scalar() or 0
    
    # Get recent activities
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    
    dashboard_data = {
        'stats': {
            'total_users': total_users,
            'total_guides': total_guides,
            'total_travelers': total_travelers,
            'total_trips': total_trips,
            'active_trips': active_trips,
            'total_bookings': total_bookings,
            'total_revenue': float(total_revenue)
        },
        'recent_users': [user.to_dict() for user in recent_users],
        'recent_bookings': [booking.to_dict() for booking in recent_bookings]
    }
    
    return success_response(dashboard_data)

@admin_bp.route('/users', methods=['GET'])
@token_required
@role_required(['admin'])
def get_users():
    page = request.args.get('page', 1, type=int)
    role = request.args.get('role')
    search = request.args.get('search')
    
    query = User.query
    
    if role:
        query = query.filter_by(role=role)
    if search:
        query = query.filter(
            db.or_(
                User.full_name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )
    
    users_data = paginate_query(query.order_by(User.created_at.desc()), page)
    return success_response(users_data)

@admin_bp.route('/users/<int:user_id>/verify', methods=['PUT'])
@token_required
@role_required(['admin'])
def verify_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return error_response('User not found', 404)
    
    user.is_verified = True
    
    # If it's a guide, also verify their profile
    if user.role == 'guide' and user.guide_profile:
        user.guide_profile.is_verified = True
    
    db.session.commit()
    
    return success_response(user.to_dict(), 'User verified successfully')

@admin_bp.route('/users/<int:user_id>/suspend', methods=['PUT'])
@token_required
@role_required(['admin'])
def suspend_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return error_response('User not found', 404)
    
    user.is_verified = False
    
    # Deactivate all trips if it's a guide
    if user.role == 'guide':
        Trip.query.filter_by(guide_id=user_id).update({'is_active': False})
    
    db.session.commit()
    
    return success_response(user.to_dict(), 'User suspended successfully')

@admin_bp.route('/trips', methods=['GET'])
@token_required
@role_required(['admin'])
def get_all_trips():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')  # active, inactive
    guide_id = request.args.get('guide_id', type=int)
    
    query = Trip.query
    
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    
    if guide_id:
        query = query.filter_by(guide_id=guide_id)
    
    trips_data = paginate_query(query.order_by(Trip.created_at.desc()), page)
    return success_response(trips_data)

@admin_bp.route('/trips/<int:trip_id>/approve', methods=['PUT'])
@token_required
@role_required(['admin'])
def approve_trip(trip_id):
    trip = Trip.query.get(trip_id)
    
    if not trip:
        return error_response('Trip not found', 404)
    
    trip.is_active = True
    db.session.commit()
    
    return success_response(trip.to_dict(), 'Trip approved successfully')

@admin_bp.route('/trips/<int:trip_id>/reject', methods=['PUT'])
@token_required
@role_required(['admin'])
def reject_trip(trip_id):
    trip = Trip.query.get(trip_id)
    
    if not trip:
        return error_response('Trip not found', 404)
    
    trip.is_active = False
    db.session.commit()
    
    return success_response(trip.to_dict(), 'Trip rejected successfully')

@admin_bp.route('/bookings', methods=['GET'])
@token_required
@role_required(['admin'])
def get_all_bookings():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    
    query = Booking.query
    
    if status:
        query = query.filter_by(status=status)
    
    bookings_data = paginate_query(query.order_by(Booking.created_at.desc()), page)
    return success_response(bookings_data)

@admin_bp.route('/payments', methods=['GET'])
@token_required
@role_required(['admin'])
def get_all_payments():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    method = request.args.get('method')
    
    query = Payment.query
    
    if status:
        query = query.filter_by(payment_status=status)
    if method:
        query = query.filter_by(payment_method=method)
    
    payments_data = paginate_query(query.order_by(Payment.created_at.desc()), page)
    return success_response(payments_data)

@admin_bp.route('/analytics/revenue', methods=['GET'])
@token_required
@role_required(['admin'])
def get_revenue_analytics():
    from datetime import datetime, timedelta
    
    # Get revenue for last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    daily_revenue = db.session.query(
        func.date(Payment.payment_date).label('date'),
        func.sum(Payment.amount).label('revenue')
    ).filter(
        Payment.payment_status == 'completed',
        Payment.payment_date >= thirty_days_ago
    ).group_by(func.date(Payment.payment_date)).all()
    
    # Revenue by payment method
    method_revenue = db.session.query(
        Payment.payment_method,
        func.sum(Payment.amount).label('revenue')
    ).filter(Payment.payment_status == 'completed').group_by(Payment.payment_method).all()
    
    analytics_data = {
        'daily_revenue': [
            {'date': str(item.date), 'revenue': float(item.revenue)}
            for item in daily_revenue
        ],
        'revenue_by_method': [
            {'method': item.payment_method, 'revenue': float(item.revenue)}
            for item in method_revenue
        ]
    }
    
    return success_response(analytics_data)