from flask import Blueprint, render_template

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

@employee_bp.route('/login')
def employee_login():
    return render_template('employee_templates/employee_login.html')

@employee_bp.route('/dashboard')
def employee_dashboard():
    return render_template('employee_templates/employee_dashboard.html')

@employee_bp.route('/client_info')
def employee_customer_info():
    return render_template('employee_templates/employee_client_info.html')

