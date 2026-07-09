import os
from dotenv import load_dotenv

# Load execution environmental ecosystem properties dynamically
load_dotenv()


class Config:
    """
    Base configuration configuration matrix for PenHex Security Backend
    """

    # Flask Application Core Secure Encryption Key
    SECRET_KEY = os.getenv("SECRET_KEY", "penhexx_default_secret_fallback_key")

    # Server Execution Variables
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t", "yes")
    PORT = int(os.getenv("PORT", 5000))
    HOST = os.getenv("HOST", "0.0.0.0")

    # Firebase Identity & Credentials Routing Path Link
    # Synchronized with 'credentials/firebase.json' layout pattern
    FIREBASE_CREDENTIALS = os.getenv(
        "FIREBASE_CREDENTIALS",
        os.path.join("credentials", "firebase.json")
    )

    # API Security Access Controls Matrix
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

    # System Logging Verbosity Threshold Profiles
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Object-style instance initialization for fast engine properties lookup across app domains
config = Config()