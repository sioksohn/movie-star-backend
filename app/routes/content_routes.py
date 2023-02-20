from app import db
from app.models.viewer import Viewer
from app.models.content import Content
from app.models.watchlist import Watchlist
from app.models.genre import Genre
from app.models.content_genre import ContentGenre
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

contents_bp = Blueprint("contents_bp", __name__, url_prefix="/contents")

@contents_bp.route("", methods=["POST"])
def create_content():
    request_body = validate_request_body(Content, request.get_json())
    new_content = Content.from_dict(request_body)

    db.session.add(new_content)
    db.session.commit() 

    return make_response(jsonify(new_content.to_dict()), 201)

@contents_bp.route("", methods=["GET"])
def get_all_contents():
    content_query = Content.query
    contents = content_query.all()
    content_response = []
    for content in contents:
        content_response.append(content.to_dict())
    
    return jsonify(content_response)

@contents_bp.route("/<content_id>", methods=["GET"])
def get_one_content(content_id):
    content = validate_model(Content, content_id)
    return jsonify(content.to_dict())

@contents_bp.route("/<content_id>",methods=["PUT"])
def update_one_content(content_id):
    content_info = validate_model(Content, content_id)
    request_body = validate_request_body(Content, request.get_json())

    content_info.poster = request_body["poster"]
    content_info.title = request_body["title"]
    content_info.date = request_body["date"]
    content_info.media_type = request_body["media_type"]
    content_info.vote_average = request_body["vote_average"]
    content_info.genre_ids = request_body["genre_ids"]

    db.session.commit()

    return make_response(jsonify(content_info.to_dict()), 200)

@contents_bp.route("/<content_id>",methods=["DELETE"])
def delete_one_content(content_id):
    content = validate_model(Content, content_id)
    
    db.session.delete(content)
    db.session.commit()
    
    return make_response(jsonify(content.to_dict()), 200)