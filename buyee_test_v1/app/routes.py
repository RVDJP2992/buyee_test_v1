from flask import Blueprint, render_template, request
from .scraper import get_ebay_prices, get_buyee_prices, compare_prices

# ✅ Define the Blueprint FIRST
main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    query = request.args.get('q')
    comparison = []
    if query:
        ebay_data = get_ebay_prices(query)
        buyee_data = get_buyee_prices(query)
        comparison = compare_prices(ebay_data, buyee_data)
    return render_template("index.html", comparison=comparison)
