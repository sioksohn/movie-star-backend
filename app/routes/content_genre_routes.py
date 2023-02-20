from app import db
from app.models.viewer import Viewer
from app.models.content import Content
from app.models.watchlist import Watchlist
from app.models.genre import Genre
from app.models.content_genre import ContentGenre
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

content_genre_bp = Blueprint("content_genre_bp", __name__, url_prefix="/content_genre")

@content_genre_bp.route("", methods=["POST"])
def create_content_genre():
    request_body = validate_request_body(ContentGenre, request.get_json())

    content = validate_model(Content, request_body["content_id"])
    genre = validate_model(Genre, request_body["genre_id"])
    
    new_content_genre = ContentGenre.from_dict(request_body)

    db.session.add(new_content_genre)
    db.session.commit()

    return make_response(jsonify(f"Content-Genre {new_content_genre.id} successfully created"), 201)

@content_genre_bp.route("", methods=["GET"])
def read_all_content_genre():
    content_genre_query = ContentGenre.query.all()

    content_genre_response = []
    for content_genre in content_genre_query:
        content_genre_response.append(content_genre.to_dict())

    return jsonify(content_genre_response)

@content_genre_bp.route("/<content_genre_id>",methods=["DELETE"])
def delete_one_content_genre(content_genre_id):
    content_genre = validate_model(ContentGenre, content_genre_id)
    
    db.session.delete(content_genre)
    db.session.commit()
    
    return make_response(jsonify(content_genre.to_dict()), 200)
