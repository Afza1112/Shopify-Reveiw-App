import os
from pymongo import MongoClient
from bson.objectid import ObjectId

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder(app):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---- Setup Mongo Client Once ----
mongo_uri = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/review_app"
client = MongoClient(mongo_uri)
db_name = os.environ.get("DB_NAME", "review_app")

def get_db():
    return client[db_name]

# ---- Review CRUD Operations ----
def insert_review(data):
    db = get_db()
    return db.reviews.insert_one(data)

def get_reviews(product_id, approved=True):
    db = get_db()
    return list(db.reviews.find(
        {"product_id": str(product_id), "approved": approved},
        {"_id": 0}
    ))

def get_pending_reviews():
    db = get_db()
    return list(db.reviews.find({"approved": False}))

def approve_review_db(review_id):
    db = get_db()
    db.reviews.update_one({"_id": ObjectId(review_id)}, {"$set": {"approved": True}})
