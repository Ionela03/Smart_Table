from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, auth
from app.routes import auth_bp, main_bp,get_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)

    db.init_app(app)

    with app.app_context():
        from app import models 

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(get_bp, url_prefix='/get')
    app.register_blueprint(main_bp)

    return app
