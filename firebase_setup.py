
import firebase_admin
from firebase_admin import credentials, firestore
import os

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK using modl-mawkuf-key.json
    and performs a connection test.
    """
    cred_path = "modl-mawkuf-key.json"

    if not os.path.exists(cred_path):
        print("--- Firebase Connection Test FAILED ---")
        print(f"Reason: Service key file not found at '{cred_path}'.")
        print("Please upload 'modl-mawkuf-key.json' to the project root.")
        return None

    try:
        # Avoid re-initializing the app
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully.")
        else:
            print("Firebase Admin SDK already initialized.")

        # Get Firestore client
        db = firestore.client()

        # Connection Test: Try to list collections (a lightweight operation)
        _ = list(db.collections())
        print("--- Firebase Connection Test SUCCEEDED ---")
        print("System is successfully connected to the Firebase cloud.")
        return db

    except Exception as e:
        print("--- Firebase Connection Test FAILED ---")
        print(f"Reason: {e}")
        return None

# Initialize Firebase and get the Firestore client
db = initialize_firebase()
