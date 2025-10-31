from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from flask import jsonify

def create_token(identity, role):
    """
    Create a JWT access token with user identity and role.
    """
    additional_claims = {"role": role}
    token = create_access_token(identity=identity, additional_claims=additional_claims)
    return token

def token_required(f):
    """
    Decorator to require a valid JWT token.
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        jwt_data = get_jwt()
        current_user_role = jwt_data.get("role")
        return f(current_user_id, current_user_role, *args, **kwargs)
    return decorated_function

def role_required(required_role):
    """
    Decorator to require a specific role in addition to a valid JWT token.
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            jwt_data = get_jwt()
            user_role = jwt_data.get("role")
            if user_role != required_role:
                return jsonify({"error": "Insufficient permissions"}), 403
            current_user_id = get_jwt_identity()
            return f(current_user_id, *args, **kwargs)
        return decorated_function
    return decorator
