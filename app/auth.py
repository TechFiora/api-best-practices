from flask_jwt_extended import create_access_token
from flask import request, jsonify
from models import User  # Import the User model to check the credentials


# This function handles user login and returns a JWT token if credentials are correct
def login():
    """
    Authenticates the user and returns a JWT token.
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # Query the user by email (username)
    user = User.query.filter_by(email=username).first()

    # If user exists and the password matches
    if user and user.password == password:
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token)

    return jsonify({"message": "Invalid credentials"}), 401
