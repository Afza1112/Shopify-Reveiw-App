from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return "Shopify Review App Running! <a href='/review/123'>Sample Product Review</a> | <a href='/admin'>Admin</a>"
