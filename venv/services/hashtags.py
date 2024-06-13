from flask import Blueprint, request, jsonify
from models.hashtag import Hashtag
from app import db

bp = Blueprint('hashtags', __name__, url_prefix='/hashtags')

@bp.route('/', methods=['GET'])
def get_hashtags():
    hashtags = Hashtag.query.all()
    return jsonify([{"id": hashtag.id, "tag": hashtag.tag} for hashtag in hashtags])
