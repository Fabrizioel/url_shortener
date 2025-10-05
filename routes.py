from flask import Blueprint, request, jsonify, redirect
from db import collection
from datetime import datetime
import string, random, validators

url = Blueprint("url", __name__)

def generate_url_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@url.route("/shortened_code")
def code():
    code = generate_url_short_code()
    return jsonify({ "code": code })