from app import db
from app.models.viewer import Viewer
from app.models.content import Content
from app.models.watchlist import Watchlist
from app.models.genre import Genre
from app.models.content_genre import ContentGenre
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

genres_bp = Blueprint("genres_bp", __name__, url_prefix="/genres")

@genres_bp.route("", methods=["POST"])
def create_genre():
    request_body = validate_request_body(Genre, request.get_json())
    new_genre = Genre.from_dict(request_body)

    db.session.add(new_genre)
    db.session.commit()

    return make_response(jsonify(new_genre.to_dict()), 201)

@genres_bp.route("", methods=["GET"])
def get_genres():
    genres = Genre.query.all()
    genre_response = []
    for genre in genres:
        genre_response.append(genre.to_dict())

    return jsonify(genre_response)

@genres_bp.route("/<genre_id>",methods=["DELETE"])
def delete_one_genre(genre_id):
    genre = validate_model(Genre, genre_id)
    
    db.session.delete(genre)
    db.session.commit()
    
    return make_response(jsonify(genre.to_dict()), 200)