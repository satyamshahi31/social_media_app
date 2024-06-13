from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.comment import Comment
from models.post import Post
from app import db

bp = Blueprint('comments', __name__, url_prefix='/comments')

@bp.route('/<int:post_id>', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    text = data.get('text')

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    new_comment = Comment(text=text, user_id=user_id, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully"}), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_comment(id):
    data = request.get_json()
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    user_id = get_jwt_identity()
    if comment.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    if 'text' in data:
        comment.text = data['text']

    db.session.commit()
    return jsonify({"message": "Comment updated successfully"})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    user_id = get_jwt_identity()
    if comment.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted successfully"})
