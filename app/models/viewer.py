from app import db

class Viewer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    watchlists = db.relationship("Watchlist", back_populates="viewer") #contents

    def to_dict(self):
        viewer_dict = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
        watched_contents = []
        for watched_content in self.watchlists:
            watched_contents.append(watched_content.to_dict())
        viewer_dict["watchlists"] = watched_contents
        
        return viewer_dict

    @classmethod
    def from_dict(cls, request_body):
        new_viewer = cls(
            name = request_body["name"],
            email = request_body["email"],
            password = request_body["password"]
        )
        return new_viewer