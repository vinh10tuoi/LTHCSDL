from urllib.parse import quote

import cloudinary
from flask import Flask
from flask_babelex import Babel
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '$@#%$^%$^%%$FGHFGHBVBSD@#$%%'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/qlhsdb?charset=utf8mb4' % quote('admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 4

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

babel = Babel(app=app)

cloudinary.config(cloud_name='dzbcst18v',
                  api_key='245414666449735',
                  api_secret='r0MlKuAj9kOoyRqgY-WQUCYUpw0')


@babel.localeselector
def load_locale():
    return 'vi'
