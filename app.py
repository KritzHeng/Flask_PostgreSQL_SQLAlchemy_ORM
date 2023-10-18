from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
print("url", url)
app.config['SQLALCHEMY_DATABASE_URI'] = url  # Use SQLite for simpli city. Replace with your preferred DB.
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use SQLite for simpli city. Replace with your preferred DB.
db = SQLAlchemy(app)
print("db", db)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email



# from flask import request, jsonify
@app.route('/')
def home():
    
    return "Hello, world"

@app.route('/users', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    new_user = User(name=name, email=email)

    # Check if user with that email already exists
    db.session.add(new_user)
    # 
    db.session.commit()
    return jsonify({'message': 'User added!'}), 201

@app.route('/users', methods=['GET'])
def get_users():
        users = User.query.all()
        return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Get the user requested by querying filter by Id the database
    user = User.query.filter_by(id=user_id).first()

    # # using get_or_404 for simplicity. You can also use first_or_404
    # user = User.query.get_or_404(user_id)
    print("user", user)
    if(user is None):
        return jsonify({'message': 'User not found!'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Get the user to update
    user = User.query.get_or_404(user_id)
    
    # Check for name in the request and update if present
    if 'name' in request.json:
        user.name = request.json['name']
    
    # Check for email in the request and update if present
    if 'email' in request.json:
        # You might want to ensure the new email isn't already used by another user.
        existing_email = User.query.filter_by(email=request.json['email']).first()
        if existing_email and existing_email.id != user_id:
            return jsonify({'message': 'Email already in use!'}), 400
        user.email = request.json['email']
    
    db.session.commit()
    return jsonify({'message': 'User updated!'}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted!'}), 200



if __name__ == '__main__':
    # db.create_all()  # This creates the database and tables if they don't exist
    app.run(debug=True)
    
