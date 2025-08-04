from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.review import (
    get_pending_reviews,
    approve_review_db,
    reject_review_db,
    amend_review_db,
    reply_review_db,
    get_review_by_id,
    get_all_reviews,
    delete_review
)

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_panel():
    """Show only pending reviews by default."""
    try:
        pending = get_pending_reviews()
        for r in pending:
            r['_id'] = str(r.get('_id', ''))
        return render_template("admin.html", reviews=pending, show_all=False)
    except Exception as e:
        return f"Admin Error: {str(e)}", 500

def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper

@admin_bp.route('/admin/all')
def all_reviews():
    """Show all reviews (pending, approved, rejected) in one table."""
    try:
        reviews = get_all_reviews()
        for r in reviews:
            r['_id'] = str(r.get('_id', ''))
        return render_template("admin.html", reviews=reviews, show_all=True)
    except Exception as e:
        return f"Admin Error: {str(e)}", 500

@admin_bp.route('/admin/approve/<review_id>', methods=['POST'])
def approve_review(review_id):
    try:
        approve_review_db(review_id)
        flash("Review approved.", "success")
        return redirect(url_for('admin.admin_panel'))
    except Exception as e:
        return f"Approval Error: {str(e)}", 500

@admin_bp.route('/admin/reject/<review_id>', methods=['POST'])
def reject_review(review_id):
    try:
        reject_review_db(review_id)
        flash("Review rejected.", "info")
        return redirect(url_for('admin.admin_panel'))
    except Exception as e:
        return f"Reject Error: {str(e)}", 500

@admin_bp.route('/admin/amend/<review_id>', methods=['POST'])
def amend_review(review_id):
    try:
        new_text = request.form.get('amend_text', '').strip()
        if not new_text:
            flash("Amendment text cannot be empty.", "warning")
            return redirect(url_for('admin.admin_panel'))
        amend_review_db(review_id, new_text)
        flash("Review amended.", "success")
        return redirect(url_for('admin.admin_panel'))
    except Exception as e:
        return f"Amend Error: {str(e)}", 500

@admin_bp.route('/admin/reply/<review_id>', methods=['POST'])
def reply_review(review_id):
    try:
        reply_text = request.form.get('reply_text', '').strip()
        if not reply_text:
            flash("Reply cannot be empty.", "warning")
            return redirect(url_for('admin.admin_panel'))
        reply_review_db(review_id, reply_text)
        flash("Reply sent.", "success")
        return redirect(url_for('admin.admin_panel'))
    except Exception as e:
        return f"Reply Error: {str(e)}", 500

@admin_bp.route('/admin/delete/<review_id>', methods=['POST'])
def delete_review_admin(review_id):
    try:
        delete_review(review_id)
        flash("Review deleted.", "danger")
        return redirect(url_for('admin.admin_panel'))
    except Exception as e:
        return f"Delete Error: {str(e)}", 500

