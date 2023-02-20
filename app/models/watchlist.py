from app import db

class Watchlist(db.Model):
    __tablename__ = "watchlist"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    viewer_id = db.Column(db.Integer, db.ForeignKey('viewer.id'), nullable=False )
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    viewer_rate = db.Column(db.Float)
    viewer_comment = db.Column(db.Text)
    viewer = db.relationship("Viewer", back_populates="watchlists")
    content = db.relationship("Content", back_populates="watchlists")


    def to_dict(self):
        watchlist_dict = {
            "watchlist_id": self.id,
            "viewer_id": self.viewer_id,
            "content_id": self.content_id,
            "viewer_rate": self.viewer_rate,
            "viewer_comment": self.viewer_comment     
        }
        return watchlist_dict

    @classmethod
    def from_dict(cls, request_body):
        new_obj = cls(
            viewer_id = request_body["viewer_id"],
            content_id = request_body["content_id"],
            viewer_rate = request_body["viewer_rate"],
            viewer_comment = request_body["viewer_comment"]
        )
        return new_obj