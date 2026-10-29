from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "esta_es_una_clave_secreta_muy_segura"
bcrypt = Bcrypt(app)