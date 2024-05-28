from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, auth
from app.models import Admin
from flask import current_app
import logging
import json
import os

auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)
get_bp = Blueprint('get', __name__)

@main_bp.route('/set_runtime', methods=['POST'])
def set_runtime():
    data = request.get_json()
    run_time = data.get('run_time')
    if run_time is None:
        return jsonify({'message': 'Missing run_time argument'}), 400
    
    # Obține calea către directorul curent al scriptului
    current_dir = os.path.dirname(os.path.abspath(__file__))
    runtime_path = os.path.join(current_dir, 'runtime.json')
    
    # Scrie run_time într-un fișier
    with open(runtime_path, 'w') as f:
        json.dump({'run_time': run_time}, f)
    
    return jsonify({'message': 'Run time set successfully'}), 200

# Verificarea parolei pentru autentificare
@auth.verify_password
def verify_password(username, password):
    user = Admin.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

@main_bp.route('/admin/delete/<string:username>', methods=['DELETE'])
def delete_admin(username):
    current_app.logger.debug(f"Attempting to delete admin: {username}")
    admin_to_delete = Admin.query.filter_by(username=username).first()
    if admin_to_delete is None:
        current_app.logger.error(f"Admin not found: {username}")
        return jsonify({'error': 'Admin not found'}), 404

    db.session.delete(admin_to_delete)
    db.session.commit()
    current_app.logger.debug(f"Admin deleted: {username}")
    return jsonify({'success': 'Admin deleted'}), 200

logging.basicConfig(level=logging.DEBUG)

@auth_bp.route('/update_credentials', methods=['POST'])
@auth.login_required
def update_credentials():
    current_app.logger.debug(f"Authenticated user: {auth.current_user().username}")
    data = request.get_json()
    current_app.logger.debug(f"Received data: {data}")
    current_password = data.get('current_password')
    new_username = data.get('new_username')
    new_password = data.get('new_password')

    admin = Admin.query.filter_by(username=auth.current_user().username).first()

    if not admin or not admin.check_password(current_password):
        current_app.logger.debug("Invalid current password")
        return jsonify({'message': 'Invalid current password'}), 401

    if new_username:
        if Admin.query.filter(Admin.username == new_username).first() is not None:
            current_app.logger.debug("Username already exists")
            return jsonify({'message': 'Username already exists'}), 409
        admin.username = new_username
    
    if new_password:
        admin.set_password(new_password)

    db.session.commit()
    current_app.logger.debug("Credentials updated successfully")
    return jsonify({'message': 'Credentials updated successfully'}), 200

@get_bp.route('/admins', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    return jsonify([admin.username for admin in admins])

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
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

@main_bp.route('/')
def index():
    return jsonify({'message': 'Welcome to the server!'})
