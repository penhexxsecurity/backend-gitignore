import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global Firestore DB instance variable
db = None


def initialize_firebase():
    """
    Initializes the Firebase Admin SDK context using local service account profiles.
    Safe for multi-threaded debug-reloader execution modes.
    """
    global db

    # Prevent re-initialization if the app context reloads
    if firebase_admin._apps:
        db = firestore.client()
        return db

    try:
        # Pull key location path from environmental properties matrix
        cred_path = os.getenv("FIREBASE_CREDENTIALS", os.path.join("credentials", "firebase.json"))

        if not os.path.exists(cred_path):
            raise FileNotFoundError(f"Firebase credentials JSON file not found at: {cred_path}")

        # Load Admin SDK credential certificate profile boundaries
        cred = credentials.Certificate(cred_path)

        # Initialize the underlying app instance context securely
        firebase_admin.initialize_app(cred)

        # Initialize the structural Firestore connection link
        db = firestore.client()

        print("✅ Firebase Admin SDK initialized successfully.")
        return db

    except Exception as e:
        print(f"❌ Firebase initialization fatal breakdown error: {str(e)}")
        raise e


def get_db():
    """
    Thread-safe contextual accessor function to retrieve the active Firestore database driver.
    """
    global db
    if db is None:
        return initialize_firebase()
    return db


# Auto-initialize core app matrix context layers upon engine bootup cycle execution hook
initialize_firebase()