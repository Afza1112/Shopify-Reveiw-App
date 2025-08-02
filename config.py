from pymongo import MongoClient
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production'
    MONGO_URI = os.environ.get("MONGO_URI") or "mongodb://localhost:27017/"
    DB_NAME = os.environ.get("DB_NAME") or "review_app"
    MONGO_CLIENT = MongoClient(MONGO_URI)
    UPLOAD_FOLDER = 'static/review_images'
