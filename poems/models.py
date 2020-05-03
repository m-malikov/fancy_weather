from poems import db


class Poem(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    weather_type = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
