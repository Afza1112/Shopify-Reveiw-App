import os
import time
from flask import Blueprint, render_template, request, jsonify, current_app, url_for, redirect, flash
from werkzeug.utils import secure_filename
from models.review import (
    insert_review, get_reviews, get_pending_reviews, get_review_by_id,
    approve_review_db, reject_review_db, amend_review_db, reply_review_db,
    delete_review, get_all_reviews
)

review_bp = Blueprint('review', __name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config.get("ALLOWED_EXTENSIONS", {'png','jpg','jpeg','gif'})

# ----- CUSTOMER FACING -----

@review_bp.route('/review/<product_id>')
def review_form(product_id):
    """Show the public review form for a product."""
    reviews = get_reviews(product_id, approved=True)
    avg_rating = 0
    if reviews:
        avg_rating = round(sum(int(r.get('rating', 0)) for r in reviews) / len(reviews), 2)
    star_counts = {i: 0 for i in range(1, 6)}
    for r in reviews:
        rating = int(r.get("rating", 0))
        if 1 <= rating <= 5:
            star_counts[rating] += 1
    star_perc = {k: round((v / len(reviews)) * 100, 1) if reviews else 0 for k, v in star_counts.items()}

    return render_template(
        'reviews_amazon.html',
        reviews=reviews,
        avg_rating=avg_rating,
        total_reviews=len(reviews),
        star_perc=star_perc,
        product_id=product_id
    )

@review_bp.route('/api/review', methods=['POST'])
def submit_review():
    """API to submit a review (handles optional image)."""
    data = request.form.to_dict()
    data['approved'] = False
    data['rejected'] = False
    data['admin_reply'] = ""
    data['created_at'] = int(time.time())
    image_url = ""
    product_id = data.get("product_id")
    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{int(time.time())}_{filename}"
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(save_path)
            image_url = url_for('static', filename=f'review_images/{filename}', _external=True)
    if image_url:
        data['image_url'] = image_url
    insert_review(data)
    return jsonify({"message": "Review submitted, pending approval."})

@review_bp.route('/api/reviews/<product_id>')
def api_reviews(product_id):
    """API to fetch all approved reviews for product."""
    reviews = get_reviews(product_id, approved=True)
    return jsonify(reviews)

# ----- ADMIN PANEL ROUTES (MODERATION) -----

@review_bp.route('/admin/approve/<review_id>', methods=['POST'])
def approve_review(review_id):
    approve_review_db(review_id)
    flash("Review approved.", "success")
    return redirect(request.referrer or url_for('admin.admin_panel'))

@review_bp.route('/admin/reject/<review_id>', methods=['POST'])
def reject_review(review_id):
    reject_review_db(review_id)
    flash("Review rejected.", "info")
    return redirect(request.referrer or url_for('admin.admin_panel'))

@review_bp.route('/admin/amend/<review_id>', methods=['POST'])
def amend_review(review_id):
    new_text = request.form.get('amend_text', '').strip()
    if not new_text:
        flash("Amendment text cannot be empty.", "warning")
        return redirect(request.referrer or url_for('admin.admin_panel'))
    amend_review_db(review_id, new_text)
    flash("Review amended.", "success")
    return redirect(request.referrer or url_for('admin.admin_panel'))

@review_bp.route('/admin/reply/<review_id>', methods=['POST'])
def reply_review(review_id):
    reply_text = request.form.get('reply_text', '').strip()
    if not reply_text:
        flash("Reply cannot be empty.", "warning")
        return redirect(request.referrer or url_for('admin.admin_panel'))
    reply_review_db(review_id, reply_text)
    flash("Reply sent.", "success")
    return redirect(request.referrer or url_for('admin.admin_panel'))

@review_bp.route('/admin/delete/<review_id>', methods=['POST'])
def delete_review_admin(review_id):
    delete_review(review_id)
    flash("Review deleted.", "danger")
    return redirect(request.referrer or url_for('admin.admin_panel'))

# ----- OPTIONAL: For admin page with all reviews -----

@review_bp.route('/admin/all')
def all_reviews():
    """Show all reviews (approved + pending) for admin."""
    reviews = get_all_reviews()
    for r in reviews:
        r['_id'] = str(r.get('_id', ''))
    return render_template("admin.html", reviews=reviews, show_all=True)

# ----- OPTIONAL: Edit review GET (for admin) -----

@review_bp.route('/admin/edit/<review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    review = get_review_by_id(review_id)
    if not review:
        flash("Review not found.", "danger")
        return redirect(url_for('admin.admin_panel'))
    if request.method == 'POST':
        new_text = request.form.get('edit_text', '').strip()
        amend_review_db(review_id, new_text)
        flash("Review updated.", "success")
        return redirect(url_for('admin.admin_panel'))
    review['_id'] = str(review.get('_id', ''))
    return render_template("edit_review.html", review=review)

# Export Blueprint for app use
__all__ = ["review_bp"]
