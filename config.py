from pymongo import MongoClient
import os

class Config:
    # ...other configs...
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecret")
    MONGO_URI = os.environ.get("MONGO_URI")
    DB_NAME = os.environ.get("DB_NAME", "review_app")
    UPLOAD_FOLDER = 'static/review_images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # <--- add this line

    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "paksa.admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Paksa@385+")  # store hashed in real apps!
