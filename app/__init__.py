from flask import Flask
from .routes import configure_routes
from .database import engine, Base

Base.metadata.create_all(bind=engine)

def create_app():
    app = Flask(__name__)
    configure_routes(app)
    return app