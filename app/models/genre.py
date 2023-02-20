from app import db

class Genre(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contents_genres = db.relationship("ContentGenre", back_populates="genre")

    def to_dict(self):
        genre_dict = {
            "id": self.id,
            "name": self.name,
        }

        genre_contents = []
        for content in self.contents_genres:
            genre_contents.append(content.to_dict())
        genre_dict["contents"] = genre_contents
        
        return genre_dict

    @classmethod
    def from_dict(cls, request_body):
        new_genre = cls(
            id = request_body["id"],
            name = request_body["name"]
        )
        return new_genre