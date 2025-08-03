import os, time
from flask import Blueprint, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from models.review import insert_review, get_reviews

review_bp = Blueprint('review', __name__)

def allowed_file(filename):
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

@review_bp.route('/api/review', methods=['POST'])
def submit_review():
    data = request.form.to_dict()
    data['approved'] = False
    image_url = ""
    # Save image if present
    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{int(time.time())}_{filename}"
            # Ensure the upload folder exists (e.g., static/review_images)
            upload_folder = os.path.join(current_app.static_folder, 'review_images')
            os.makedirs(upload_folder, exist_ok=True)
            save_path = os.path.join(upload_folder, filename)
            file.save(save_path)
            image_url = url_for('static', filename=f'review_images/{filename}', _external=True)
    if image_url:
        data['image_url'] = image_url
    insert_review(data)
    return jsonify({"message": "Review submitted, pending approval."})

@review_bp.route('/api/reviews/<product_id>')
def api_reviews(product_id):
    reviews = get_reviews(product_id, approved=True)
    return jsonify(reviews)
