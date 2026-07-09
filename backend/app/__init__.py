from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)

    # Enable CORS for frontend (React)
    CORS(app)

    # Config
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "penhexx-default-secret")

    # Import and register routes
    from app.routes.contact_routes import contact_bp
    from app.routes.general_routes import general_bp
    from app.routes.enterprise_routes import enterprise_bp

    app.register_blueprint(contact_bp, url_prefix="/api/contact")
    app.register_blueprint(general_bp, url_prefix="/api/general")
    app.register_blueprint(enterprise_bp, url_prefix="/api/enterprise")

    @app.route("/")
    def home():
        return {
            # 2026 Structured standard clean layout
            "status": "success",
            "message": "PenHex Security Backend Running 🚀",
            "version": "1.0.0"
        }

    return app