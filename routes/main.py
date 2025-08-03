from flask import Blueprint, render_template, redirect, url_for, request
from models.review import get_reviews

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Optional: Redirect to a specific product or a landing page
    # You might want to show a message or instructions instead of redirect
    return "<h2>Welcome! Add /reviews/&lt;product_id&gt; to the URL to view reviews for that Shopify product.</h2>"

@main_bp.route('/reviews/<product_id>')
def review_amazon(product_id):
    reviews = get_reviews(product_id, approved=True)
    total_reviews = len(reviews)
    avg_rating = 0
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
