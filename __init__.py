from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuration settings
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['DATABASE_URI'] = 'postgresql://postgres:ayushi%400987@localhost:5000/Image_processing'
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    app.config['PROCESSED_FOLDER'] = 'app/static/processed'

    # Import and register Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Initialize database connection if needed
    # Add other initializations here (e.g., extensions, database connections)

    return app
