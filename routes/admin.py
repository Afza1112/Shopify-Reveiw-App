from flask import Blueprint, render_template, redirect, url_for, request
from models.review import reviews
from bson.objectid import ObjectId

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin():
    try:
        pending = list(reviews.find({"approved": False}))
        for r in pending:
            r['_id'] = str(r.get('_id', ''))
        return render_template("admin.html", reviews=pending)
    except Exception as e:
        return f"Admin Error: {str(e)}", 500

@admin_bp.route('/admin/approve/<review_id>', methods=['POST'])
def approve_review(review_id):
    try:
        reviews.update_one({"_id": ObjectId(review_id)}, {"$set": {"approved": True}})
        return redirect(url_for('admin.admin'))
    except Exception as e:
        return f"Approval Error: {str(e)}", 500
