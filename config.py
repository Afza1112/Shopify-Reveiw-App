import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    MONGO_URI = os.getenv("MONGO_URI")
    UPLOAD_FOLDER = os.path.join("static", "review_images")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
