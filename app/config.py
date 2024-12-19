class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"  # Database URI (SQLite in this case)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
    JWT_SECRET_KEY = "your-secret-key"  # Secret key for JWT
    CACHE_TYPE = "SimpleCache"  # For Flask-Caching
