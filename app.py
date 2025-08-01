from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os, time

load_dotenv()
app = Flask(__name__)

client = MongoClient(os.environ.get("MONGO_URI"))
db = client["mongo"]
reviews = db.reviews

UPLOAD_FOLDER = 'static/review_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return "Shopify Review App Running! <a href='/review/123'>Sample Product Review</a> | <a href='/admin'>Admin</a>"

@app.route('/review/<product_id>')
def review_form(product_id):
    return render_template('review_form.html', product_id=product_id)

@app.route('/api/review', methods=['POST'])
def submit_review():
    data = request.form.to_dict()
    data['approved'] = False
    image_url = ""
    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{int(time.time())}_{filename}"  # To avoid overwrite
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            image_url = url_for('static', filename='review_images/' + filename, _external=True)
    if image_url:
        data['image_url'] = image_url
    reviews.insert_one(data)
    return jsonify({"message": "Review submitted, pending approval."})

@app.route('/api/reviews/<product_id>')
def get_reviews(product_id):
    approved_reviews = list(reviews.find({"product_id": product_id, "approved": True}, {"_id": 0}))
    return jsonify(approved_reviews)

@app.route('/admin')
def admin():
    pending = list(reviews.find({"approved": False}))
    # Convert _id (ObjectId) to string for Jinja rendering
    for r in pending:
        r['_id'] = str(r['_id'])
    return render_template('admin.html', reviews=pending)

@app.route('/admin/approve/<review_id>', methods=['POST'])
def approve_review(review_id):
    reviews.update_one({"_id": ObjectId(review_id)}, {"$set": {"approved": True}})
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
