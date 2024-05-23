from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import Admin
import logging

auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)
get_bp=Blueprint('get',__name__)

@auth_bp.route('/validate_credentials', methods=['POST'])
def validate_credentials():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    admin = Admin.query.filter_by(username=username).first()
    if admin and check_password_hash(admin.password_hash, password):
        return jsonify({'message': 'Credentials validated'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


logging.basicConfig(level=logging.DEBUG)

@auth_bp.route('/update_credentials', methods=['POST'])
#  to be defined

@get_bp.route('/admins', methods=['GET'])
def get_admins():
    admins=Admin.query.all()
    return jsonify([admin.username for admin in admins])

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Obține datele trimise prin POST ca JSON
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = Admin.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if username is None or password is None:
        return jsonify({'message': 'Missing arguments'}), 400
    if Admin.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'User already exists'}), 400

    user = Admin(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201


#@app.route('/delete_admin/<username>', methods=['DELETE'])
#to be defined


@main_bp.route('/')
def index():
    return jsonify({'message': 'Welcome to the server!'})