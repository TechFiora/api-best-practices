from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from flask_caching import Cache
from flask_migrate import Migrate
import logging
from models import db, User  # Import User model from models.py
from auth import login  # Import login function from auth.py

# 1. Initialize the Flask app
app = Flask(__name__)
app.config.from_object("config.Config")  # Load the config from config.py

# 2. Initialize extensions
db.init_app(app)  # Initialize SQLAlchemy with the app
jwt = JWTManager(app)  # Flask-JWT-Extended for authentication
migrate = Migrate(app, db)  # Flask-Migrate for database migrations
cache = Cache(
    app, config={"CACHE_TYPE": "SimpleCache"}
)  # Flask-Caching for performance

# 3. Setup for logging
logging.basicConfig(level=logging.DEBUG)


# 4 Dummy data
with app.app_context():
    db.create_all()

    # Füge Dummy-Daten hinzu, wenn keine Benutzer existieren
    user = User.query.get(1)
    if User.query.count() == 0:
        dummy_user = User(
            id=1, name="John Doe", email="john.doe@example.com", password="password123"
        )
        db.session.add(dummy_user)
        db.session.commit()
        app.logger.info("Dummy user created")


# 5. Route to get a user by ID (public route)
@app.route("/v1/users/<int:id>", methods=["GET"])
@cache.cached(timeout=50)  # Cache the response to improve performance
def get_user(id):
    """
    Retrieve a user from the database and return details.
    """
    user = User.query.get(id)
    if user is None:
        app.logger.error(f"User with id {id} not found")
        return jsonify({"message": "User not found"}), 404
    return jsonify({"id": user.id, "name": user.name, "email": user.email})


# 6. Route for user login (authentication route)
@app.route("/login", methods=["POST"])
def login_route():
    """
    Route for logging in a user and returning a JWT token.
    """
    return login()


# 7. Protected route (requires authentication)
@app.route("/protected", methods=["GET"])
@jwt_required()  # Protected route, requires valid JWT token
def protected():
    """
    A protected endpoint that requires authentication to access.
    """
    return jsonify(message="This is a protected endpoint")


# 8. Error handling (optional)
@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors.
    """
    app.logger.error(f"404 error: {error}")
    return jsonify({"message": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors (internal server errors).
    """
    app.logger.error(f"500 error: {error}")
    return jsonify({"message": "Internal server error"}), 500


# 9. Run the app
if __name__ == "__main__":
    app.run(debug=True)
