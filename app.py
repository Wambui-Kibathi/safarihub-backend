from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from utils.db import db
from routes.auth_routes import auth_bp
from routes.destination_routes import destination_bp
from routes.guide_routes import guide_bp
from routes.payment_routes import payment_bp
from routes.traveler_routes import traveler_bp
from routes.email_routes import email_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(destination_bp, url_prefix='/destinations')
app.register_blueprint(guide_bp, url_prefix='/guides')
app.register_blueprint(payment_bp, url_prefix='/payments')
app.register_blueprint(traveler_bp, url_prefix='/travelers')
app.register_blueprint(email_bp, url_prefix='/email')

@app.route('/')
def home():
    return {"message": "SafariHub backend is live!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
