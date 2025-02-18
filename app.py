from flask import Flask, render_template
from models import db, User, Farmer, Vet
from dotenv import load_dotenv
import os
from flask_migrate import Migrate

# load environment variables from .env
load_dotenv()


# Fetch database credentials from environment variables
db_host = os.getenv("MYSQL_HOST", "localhost")
db_user = os.getenv("MYSQL_USER", "root")
db_password = os.getenv("MYSQL_PwD")
db_name = os.getenv("MYSQL_DB")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():

    return render_template('index.html')


@app.route('/login')
def login():

    return render_template('login.html')


@app.route('/register')
def register():

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)