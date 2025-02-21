from services.client_service import ClientService
from flask import Blueprint, jsonify, render_template, redirect, request

client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.route('/signup')
def client_signup():
    """return client sign up page"""
    return render_template('client_templates/client_signup.html')

@client_bp.route('/login')
def client_login():
    """return client login page"""
    return render_template('client_templates/client_login.html')

@client_bp.route('/login', methods=['POST'])
def client_login_post():
    """handling login request"""
    print(f'get client login request: {request.json}')
    username = request.json.get('username')
    password = request.json.get('password')
    client_service = ClientService(client_id=username)
    print(f'username: {username}, password: {password}')
    if client_service.handle_login(password):
        return jsonify({
            'status': 'success',
            'redirect_url': '/client/dashboard'
        }), 200
    else:
        return jsonify({
            'status': 'failed',
        }), 401

@client_bp.route('/dashboard')
def client_dashboard():
    """return client dashboard"""
    return render_template('client_templates/client_dashboard.html', username='Client User')
@client_bp.route('/transfer')
def client_transfer():
    """return client transfer page"""
    return render_template('client_templates/client_transfer.html')

@client_bp.route('/setting')
def client_setting():
    """return client_setting page"""
    return render_template('client_templates/client_setting.html')

@client_bp.route('/auth/verify')
def client_verify():
    """return verification code page"""
    return render_template('components/verify.html')
