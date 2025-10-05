from flask import Blueprint, request, jsonify, redirect
from db import collection
from datetime import datetime, timedelta
import string, random, validators

url = Blueprint("url", __name__)

def generate_url_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def get_expires_at_date():
    now = datetime.now()
    expires_at_date = now + timedelta(days=30)
    return expires_at_date

@url.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url or not validators.url(original_url):
        return jsonify({ "error": "Invalid URL." }), 400
    
    existing = collection.find_one({ "original_url": original_url })
    if existing:
        short_code = existing["short_code"]
        return jsonify({ "short_url": f"http://localhost:5000/{short_code}" })
    
    short_code = generate_url_short_code()
    expires_at_date = get_expires_at_date()

    collection.insert_one({
        "original_url": original_url,
        "short_code": short_code,
        "clicks": 0,
        "created_at": datetime.now(),
        "expires_at": expires_at_date
    })

    return jsonify({
        "original_url": original_url,
        "short_url": f"http://localhost:5000/{short_code}",
        "expires_at": expires_at_date
    })

@url.route("/<string:short_code>")
def redirect_url(short_code):
    url = collection.find_one({ "short_code": short_code })
    if not url:
        return jsonify({ "error": "URL not found." }), 404
    
    collection.update_one({ "short_code": short_code }, {"$inc": {"clicks": 1}})
    return redirect(url["original_url"])