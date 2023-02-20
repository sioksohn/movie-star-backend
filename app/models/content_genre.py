from app import db

class ContentGenre(db.Model):
    __tablename__ = "content_genre"  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False )
    content = db.relationship("Content", back_populates="contents_genres")
    genre = db.relationship("Genre", back_populates="contents_genres")

    def to_dict(self):
        content_genre_dict = {
            "content_genre_id": self.id,
            "content_id": self.content_id,
            "genre_id": self.genre_id,    
        }
        return content_genre_dict

    @classmethod
    def from_dict(cls, request_body):
        new_obj = cls(
            content_id = request_body["content_id"],
            genre_id = request_body["genre_id"],
        )
        return new_obj