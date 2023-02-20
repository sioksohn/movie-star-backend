from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.content import Content
    from app.models.viewer import Viewer
    from app.models.genre import Genre
    from app.models.content_genre import ContentGenre
    from app.models.watchlist import Watchlist

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes.content_routes import contents_bp
    app.register_blueprint(contents_bp)

    from .routes.viewer_routes import viewers_bp
    app.register_blueprint(viewers_bp)

    from .routes.genre_routes import genres_bp
    app.register_blueprint(genres_bp)

    from .routes.content_genre_routes import content_genre_bp
    app.register_blueprint(content_genre_bp)

    from .routes.watchlist_routes import watchlist_bp
    app.register_blueprint(watchlist_bp)

    return app