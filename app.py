from flask import Flask, render_template
from models import db, User, Farmer, Vet

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/vet_booking'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)

@app.route('/')
def home():

    return render_template('index.html')

@app.route('/login')
def login():

    return render_template('login.html')

if __name__ == '__main__':
    # with app.app_context():
    #     try:
    #         db.create_all()
    #         print("Database tables created successfully.")
    #     except Exception as e:
    #         print(f"Error creating tables: {e}")

    app.run(debug=True)