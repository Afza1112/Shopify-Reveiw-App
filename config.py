from pymongo import MongoClient
import os

class Config:
    # ...other configs...
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecret")
    MONGO_URI = os.environ.get("MONGO_URI")
    DB_NAME = os.environ.get("DB_NAME", "review_app")
    UPLOAD_FOLDER = 'static/review_images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # <--- add this line
