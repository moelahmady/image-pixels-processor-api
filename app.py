# app.py
from flask import Flask
from app.routes import configure_routes
from dotenv import load_dotenv
import os

load_dotenv()  # Ensure this loads the .env file
PORT = os.getenv('PORT')

app = Flask(__name__)
configure_routes(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=PORT)