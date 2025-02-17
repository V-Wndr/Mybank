from flask import Flask, render_template, request
from routes.client_routes import client_bp

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('client_login.html', name='123')

app.register_blueprint(client_bp)

if __name__ == '__main__':
    app.run(debug=True)
