from flask import Blueprint, render_template, redirect, url_for, request
from models.review import get_pending_reviews, approve_review_db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin():
    pending = get_pending_reviews()
    # Convert _id to string for Jinja
    for r in pending:
        r['_id'] = str(r['_id'])
    return render_template('admin.html', reviews=pending)

@admin_bp.route('/admin/approve/<review_id>', methods=['POST'])
def approve_review(review_id):
    approve_review_db(review_id)
    return redirect(url_for('admin.admin'))
