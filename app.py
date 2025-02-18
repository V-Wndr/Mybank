from flask import Flask, render_template
from routes.web.client_routes import client_bp
from routes.web.employee_routes import employee_bp

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('client_templates/client_login.html', name='123')

app.register_blueprint(client_bp)
app.register_blueprint(employee_bp)

if __name__ == '__main__':
    app.run(debug=True)
