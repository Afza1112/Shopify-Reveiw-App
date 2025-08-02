import os, time
from flask import Blueprint, render_template, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from models.review import insert_review, get_reviews

review_bp = Blueprint('review', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@review_bp.route('/review/<product_id>')
def review_form(product_id):
    return render_template('review_form.html', product_id=product_id)

@review_bp.route('/api/review', methods=['POST'])
def submit_review():
    data = request.form.to_dict()
    data['approved'] = False
    image_url = ""
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
    reviews = get_reviews(product_id, approved=True)
    return jsonify(reviews)
    
@main_bp.route('/review/<product_id>')
def review_amazon(product_id):
    reviews = get_reviews(product_id, approved=True)
    avg_rating, total_reviews, star_perc = get_review_summary(reviews)
    # convert perc to {5: %, 4: %, ...}
    star_perc = {k: star_perc.get(k, 0) for k in range(5, 0, -1)}
    return render_template(
        "reviews_amazon.html",
        reviews=reviews,
        avg_rating=avg_rating,
        total_reviews=total_reviews,
        star_perc=star_perc
    )
