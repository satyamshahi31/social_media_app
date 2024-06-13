from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from app import db

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name, "mobile_no": user.mobile_no, "email": user.email} for user in users])

@bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"name": user.name, "mobile_no": user.mobile_no, "email": user.email})

@bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if 'name' in data:
        user.name = data['name']
    if 'mobile_no' in data:
        if User.query.filter_by(mobile_no=data['mobile_no']).first():
            return jsonify({"error": "Mobile number already exists"}), 400
        user.mobile_no = data['mobile_no']
    if 'email' in data:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 400
        user.email = data['email']

    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})
