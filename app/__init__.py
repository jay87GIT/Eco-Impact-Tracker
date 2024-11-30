from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import routes
    from app.routes import auth, main, challenges, community
    from app.models import User

    # Register context processors
    @app.context_processor
    def utility_processor():
        from datetime import datetime
        return {
            'now': datetime.utcnow()
        }

    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.main)
    app.register_blueprint(challenges.bp)
    app.register_blueprint(community.bp)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
