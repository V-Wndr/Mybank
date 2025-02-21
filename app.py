from flask import Flask
from routes.client_routes import client_bp
from routes.employee_routes import employee_bp
from dotenv import load_dotenv
from dao import db
from dao.models import Base
from dao.demo_data import init_demo_data


# load master key from environment variables
load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# 创建所有表
with app.app_context():
    Base.metadata.create_all(db.engine)
    init_demo_data(db)

# Register blueprints
app.register_blueprint(client_bp)
app.register_blueprint(employee_bp)

if __name__ == '__main__':
    try:
        app.run(
            host='localhost',
            port=5000,
            ssl_context='adhoc',
            debug=True
        )
    except Exception as e:
        print(f"Error raised during start: {e}")
