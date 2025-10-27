from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    return {"message": "SafariHub backend is live!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
