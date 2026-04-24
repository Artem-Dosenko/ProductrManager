from flask import Flask
from models import init_db

from product.routes import product_bp
from auth.routes import auth_bp
app = Flask(__name__)
app.secret_key = '123'
init_db()


'''BLUEPRINT registration'''
app.register_blueprint(product_bp)
app.register_blueprint(auth_bp)

app.run(debug=True)