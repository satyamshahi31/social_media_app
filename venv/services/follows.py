from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.follow import Follow
from app import db

bp = Blueprint('follows', __name__, url_prefix='/follows')

@bp.route('/<int:user_id>', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id == user_id:
        return jsonify({"error": "You cannot follow yourself"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if Follow.query.filter_by(follower_id=current_user_id, followed_id=user_id).first():
        return jsonify({"error": "Already following this user"}), 400

    new_follow = Follow(follower_id=current_user_id, followed_id=user_id)
    db.session.add(new_follow)
    db.session.commit()

    return jsonify({"message": "User followed successfully"}), 201

@bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def unfollow_user(user_id):
    current_user_id = get_jwt_identity()

    follow = Follow.query.filter_by(follower_id=current_user_id, followed_id=user_id)
