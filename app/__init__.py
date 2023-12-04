from flask import Flask
from os import path
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app


if __name__ == '__main__':
    app = create_app()  

    app.run()
