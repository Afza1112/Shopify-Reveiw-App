from flask import Blueprint, render_template, redirect, url_for, request
from models.review import get_pending_reviews, approve_review_db
from bson.objectid import ObjectId  # Only if you need for extra manual queries (not in this code)

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_panel():
    try:
        # Use the helper function to get pending reviews (NO direct db/reviews usage!)
        pending = get_pending_reviews()
        for r in pending:
            r['_id'] = str(r.get('_id', ''))
        return render_template("admin.html", reviews=pending)
    except Exception as e:
        return f"Admin Error: {str(e)}", 500

@admin_bp.route('/admin/approve/<review_id>', methods=['POST'])
def approve_review(review_id):
    try:
        # Use the helper function to approve review
        approve_review_db(review_id)
        return redirect(url_for('admin.admin_panel'))
    except Exception as e:
        return f"Approval Error: {str(e)}", 500
