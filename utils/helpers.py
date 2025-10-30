from flask import jsonify
import re
from datetime import datetime

def success_response(data=None, message="Success", status_code=200):
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message="An error occurred", status_code=400, errors=None):
    response = {"success": False, "message": message}
    if errors:
        response["errors"] = errors
    return jsonify(response), status_code

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    # Kenyan phone number validation
    pattern = r'^(\+254|254|0)?[17]\d{8}$'
    return re.match(pattern, phone) is not None

def format_phone_number(phone):
    # Convert to international format
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'):
        phone = '254' + phone[1:]
    elif phone.startswith('254'):
        pass
    else:
        phone = '254' + phone
    return phone

def paginate_query(query, page, per_page=10):
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        'items': [item.to_dict() for item in items],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }

def calculate_trip_price(base_price, participants, duration_days):
    # Simple pricing logic
    total = base_price * participants
    if duration_days > 7:
        
        total *= 0.9  # 10% discount for longer trips
    return round(total, 2)