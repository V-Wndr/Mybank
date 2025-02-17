from flask import Blueprint, render_template

client_bp = Blueprint('client', __name__, url_prefix='/client')


@client_bp.route('/signup')
def client_signup():
    return render_template('client_signup.html')

@client_bp.route('/login')
def client_login():
    return render_template('client_login.html')

@client_bp.route('/dashboard')
def client_dashboard():
    return render_template('client_dashboard.html', username='Client User')
@client_bp.route('/transfer')
def client_transfer():
    return render_template('client_transfer.html')

@client_bp.route('/setting')
def client_setting():
    return render_template('client_setting.html')

@client_bp.route('/auth/verify')
def client_verify():
    return render_template('client_verify.html')
