from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.post import Post
from models.hashtag import Hashtag
from app import db

bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()
    text = data.get('text')
    image = data.get('image')
    hashtags = data.get('hashtags', [])

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_post = Post(text=text, image=image, author=user)
    for tag in hashtags:
        hashtag = Hashtag.query.filter_by(tag=tag).first()
        if not hashtag:
            hashtag = Hashtag(tag=tag)
        new_post.hashtags.append(hashtag)

    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created successfully"}), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
    data = request.get_json()
    post = Post.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    user_id = get_jwt_identity()
    if post.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    if 'text' in data:
        post.text = data['text']
    if 'image' in data:
        post.image = data['image']
    if 'hashtags' in data:
        post.hashtags = []
        for tag in data['hashtags']:
            hashtag = Hashtag.query.filter_by(tag=tag).first()
            if not hashtag:
                hashtag = Hashtag(tag=tag)
            post.hashtags.append(hashtag)

    db.session.commit()
    return jsonify({"message": "Post updated successfully"})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    user_id = get_jwt_identity()
    if post.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"})

@bp.route('/search_by_tag', methods=['GET'])
def get_posts_by_tag():
    tag = request.args.get('tag')
    hashtag = Hashtag.query.filter_by(tag=tag).first()
    if not hashtag:
        return jsonify({"error": "Hashtag not found"}), 404

    posts = hashtag.posts
    return jsonify([{"id": post.id, "text": post.text, "image": post.image, "created_on": post.created_on, "user_id": post.user_id} for post in posts])

@bp.route('/search_by_text', methods=['GET'])
def get_posts_by_text():
    text = request.args.get('text')
    posts = Post.query.filter(Post.text.like(f'%{text}%')).all()
    return jsonify([{"id": post.id, "text": post.text, "image": post.image, "created_on": post.created_on, "user_id": post.user_id} for post in posts])
