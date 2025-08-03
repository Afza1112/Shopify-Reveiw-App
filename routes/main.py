from flask import Blueprint, render_template
from models.review import get_reviews  # Make sure this is in models/review.py!

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Home with links to a sample product and admin, rendered using base.html for styling
    return render_template("base.html", title="Shopify Review App")

# Amazon-style Review Page
@main_bp.route('/reviews/amazon/<product_id>')
def review_amazon(product_id):
    reviews = get_reviews(product_id, approved=True)
    # Calculate average rating, total, and star breakdown for display
    avg_rating = 0
    total_reviews = len(reviews)
    star_counts = {i: 0 for i in range(1, 6)}
    for r in reviews:
        rating = int(r.get("rating", 0))
        if 1 <= rating <= 5:
            star_counts[rating] += 1
    if total_reviews > 0:
        avg_rating = round(sum(int(r.get("rating", 0)) for r in reviews) / total_reviews, 2)
    star_perc = {k: round((v / total_reviews) * 100, 1) if total_reviews else 0 for k, v in star_counts.items()}

    return render_template(
        "reviews_amazon.html",
        reviews=reviews,
        avg_rating=avg_rating,
        total_reviews=total_reviews,
        star_perc=star_perc
    )
