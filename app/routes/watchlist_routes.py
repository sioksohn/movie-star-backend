from app import db
from app.models.viewer import Viewer
from app.models.content import Content
from app.models.watchlist import Watchlist
from app.models.genre import Genre
from app.models.content_genre import ContentGenre
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

watchlist_bp = Blueprint("watchlist_bp", __name__, url_prefix="/watchlist")

@watchlist_bp.route("", methods=["POST"])
def create_watchlist():
    request_body = validate_request_body(Watchlist, request.get_json())
    viewer = validate_model(Viewer, request_body["viewer_id"])
    content = validate_model(Content, request_body["content_id"])
    new_watchlist = Watchlist.from_dict(request_body)

    db.session.add(new_watchlist)
    db.session.commit()

    return make_response(jsonify(f"Watchlist {new_watchlist.id} successfully created"), 201)

@watchlist_bp.route("", methods=["GET"])
def read_all_watchlists():
    watchlist_query = Watchlist.query.all()
    watchlist_response = []
    for watchlist in watchlist_query:
        watchlist_response.append(watchlist.to_dict())
    return jsonify(watchlist_response)

@watchlist_bp.route("/<watchlist_id>", methods=["DELETE"])
def delete_one_watchlist(watchlist_id):
    watchlist = validate_model(Watchlist, watchlist_id)
    
    db.session.delete(watchlist)
    db.session.commit()
    
    return make_response(jsonify(watchlist.to_dict()), 200)

@watchlist_bp.route("<viewer_id>/add", methods=["POST"]) # request = {viewer_id, content, viewer_rate, viewer_comment}
def add_one_content_to_watchlist_of_loggined_viewer(viewer_id):
    request_body = request.get_json()

    request_content = validate_request_body(Content, request_body["content"])
    viewer = validate_model(Viewer, request_body["viewer_id"])
    content = Content.query.get(request_content["id"]) ##check if the content is not new and already in the db.

    if not content: ## no relationships
        new_content = Content.from_dict(request_content)
        db.session.add(new_content)
        db.session.commit() ##1. commit to Content
    
        content = new_content
        genre_ids = content.genre_ids
        for genre_id in content.genre_ids:
            new_obj = { "content_id" :content.id, "genre_id": genre_id}
            new_content_genre = ContentGenre.from_dict(new_obj)            
            db.session.add(new_content_genre)
            db.session.commit() ##2. commit to ContentGenre

        request_watchlist = {
                "viewer_id":viewer.id,
                "content_id":content.id,
                "viewer_rate":request_body["viewer_rate"],
                "viewer_comment":request_body["viewer_comment"]
            }
        new_watchlist = Watchlist.from_dict(request_watchlist)

        db.session.add(new_watchlist)
        db.session.commit() ##3. commit to Watchlist

        
        return make_response(jsonify(f"Content{new_content.id}, Content-Genre {new_content_genre.id}, and Watchlist {new_watchlist.id} are successfully created"), 201)
    
    else: ## possibility of the duplicated relationship in the watchlist

        duplicate_watchlist = Watchlist.query.filter_by(content_id=content.id).filter_by(viewer_id=viewer.id).all()
        if not duplicate_watchlist:
            request_watchlist = {
                "viewer_id":viewer.id,
                "content_id":content.id,
                "viewer_rate":request_body["viewer_rate"],
                "viewer_comment":request_body["viewer_comment"]
            }
            new_watchlist = Watchlist.from_dict(request_watchlist)

            db.session.add(new_watchlist)
            db.session.commit()
            return make_response(jsonify(f"Watchilist{new_watchlist.id} is successfully created"), 201)
    return make_response(jsonify(f"This content already exists in the watchlist."), 400)