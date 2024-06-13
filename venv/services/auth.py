from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from app import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    mobile_no = data.get('mobile_no')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(mobile_no=mobile_no).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "User with given mobile number or email already exists."}), 400

    new_user = User(name=name, mobile_no=mobile_no, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200
