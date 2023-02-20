from app import db

class Content(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    poster = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    media_type = db.Column(db.String, nullable=False)
    vote_average = db.Column(db.Float, nullable=False)
    genre_ids = db.Column(db.ARRAY(db.Integer))
    watchlists = db.relationship("Watchlist", back_populates="content") #viewers
    contents_genres = db.relationship("ContentGenre", back_populates="content")

    def to_dict(self):
        content_dict = {
            "id" :self.id, 
            "poster" :self.poster,
            "title" :self.title, 
            "date" :self.date, 
            "media_type" :self.media_type, 
            "vote_average" :self.vote_average,
            "genre_ids": self.genre_ids
        }

        watched_users = []
        for watched_viewer in self.watchlists:
            watched_users.append(watched_viewer.to_dict())
        content_dict["watchlists"] = watched_users


        content_genres_response = []
        
        for genre in self.contents_genres:
            content_genres_response.append(genre.to_dict())
        content_dict["contents_genres"] = content_genres_response


        return content_dict

    @classmethod
    def from_dict(cls, request_body):
        new_content = cls(
            id = request_body["id"],
            poster = request_body["poster"],
            title = request_body["title"],
            date = request_body["date"],
            media_type = request_body["media_type"],
            vote_average = request_body["vote_average"],
            genre_ids = request_body["genre_ids"]
        )
        return new_content
