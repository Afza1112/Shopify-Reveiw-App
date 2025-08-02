from flask import current_app
from pymongo import MongoClient

def get_db():
    client = MongoClient(current_app.config['MONGO_URI'])
    db = client.get_default_database() or client["review_app"]
    return db

def insert_review(data):
    db = get_db()
    return db.reviews.insert_one(data)

def get_reviews(product_id, approved=True):
    db = get_db()
    return list(db.reviews.find({"product_id": product_id, "approved": approved}, {"_id": 0}))

def get_pending_reviews():
    db = get_db()
    return list(db.reviews.find({"approved": False}))

def approve_review_db(review_id):
    db = get_db()
    from bson.objectid import ObjectId
    db.reviews.update_one({"_id": ObjectId(review_id)}, {"$set": {"approved": True}})
