import os
import time
from pymongo import MongoClient
from bson.objectid import ObjectId

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if filename has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder(app):
    """Ensure the upload folder exists (called in app.py)."""
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_client():
    """Get a new Mongo client."""
    mongo_uri = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/"
    return MongoClient(mongo_uri)

def get_db():
    """Get the correct DB using env DB_NAME or default."""
    db_name = os.environ.get("DB_NAME") or "review_app"
    return get_client()[db_name]

def insert_review(data):
    """Insert a new review dict into DB."""
    db = get_db()
    data.setdefault("approved", False)
    data.setdefault("rejected", False)
    data.setdefault("admin_reply", "")
    data.setdefault("created_at", int(time.time()))
    return db.reviews.insert_one(data)

def get_reviews(product_id, approved=True):
    """Return all approved reviews for a product_id as list (no _id)."""
    db = get_db()
    return list(db.reviews.find(
        {"product_id": str(product_id), "approved": approved, "rejected": False},
        {"_id": 0}
    ))

def get_all_reviews():
    """Return all reviews for admin (all products, sorted newest first)."""
    db = get_db()
    return list(db.reviews.find().sort([("created_at", -1)]))

def get_pending_reviews():
    """Return all reviews not yet approved (not rejected)."""
    db = get_db()
    return list(db.reviews.find({"approved": False, "rejected": {"$ne": True}}).sort([("created_at", -1)]))

def get_review_by_id(review_id):
    """Return one review by its ObjectId (for admin actions)."""
    db = get_db()
    return db.reviews.find_one({"_id": ObjectId(review_id)})

def approve_review_db(review_id):
    """Mark a review as approved by its ObjectId."""
    db = get_db()
    db.reviews.update_one({"_id": ObjectId(review_id)}, {"$set": {"approved": True, "rejected": False}})

def reject_review_db(review_id):
    """Mark a review as rejected (will not show on frontend)."""
    db = get_db()
    db.reviews.update_one({"_id": ObjectId(review_id)}, {"$set": {"approved": False, "rejected": True}})

def amend_review_db(review_id, new_text):
    """Edit/amend a review text by admin."""
    db = get_db()
    db.reviews.update_one({"_id": ObjectId(review_id)}, {"$set": {"text": new_text}})

def reply_review_db(review_id, reply_text):
    """Admin reply to a customer review."""
    db = get_db()
    db.reviews.update_one({"_id": ObjectId(review_id)}, {"$set": {"admin_reply": reply_text}})

def delete_review(review_id):
    """Delete a review by its ObjectId."""
    db = get_db()
    db.reviews.delete_one({"_id": ObjectId(review_id)})

def count_reviews(product_id):
    """Count all approved reviews for a product_id."""
    db = get_db()
    return db.reviews.count_documents({"product_id": str(product_id), "approved": True, "rejected": False})

def avg_rating(product_id):
    """Average rating for a product."""
    db = get_db()
    pipeline = [
        {"$match": {"product_id": str(product_id), "approved": True, "rejected": False}},
        {"$group": {"_id": None, "avg": {"$avg": "$rating"}}}
    ]
    result = list(db.reviews.aggregate(pipeline))
    return result[0]["avg"] if result else None

def get_review_summary(reviews):
    """Return average, total, and star breakdown from reviews list."""
    total = len(reviews)
    star_counts = {s: 0 for s in range(1, 6)}
    for r in reviews:
        star_counts[int(r['rating'])] += 1
    avg = round(sum(int(r['rating']) for r in reviews) / total, 2) if total else 0
    perc = {s: round(star_counts[s] * 100 / total) if total else 0 for s in range(1, 6)}
    return avg, total, perc
