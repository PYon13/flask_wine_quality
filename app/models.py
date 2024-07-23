from app import db

class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    fixed_acidity = db.Column(db.Float)
    volatile_acidity = db.Column(db.Float)
    critic_acid = db.Column(db.Float)
    residual_sugar = db.Column(db.Float)
    chlorides = db.Column(db.Float)
    free_sulfur_dioxide = db.Column(db.Float)
    total_sulfur_dioxide = db.Column(db.Float)
    density = db.Column(db.Float)
    pH = db.Column(db.Float)
    sulphates = db.Column(db.Float)
    alcohol = db.Column(db.Float)
    quality = db.Column(db.Integer)

    def __repr__(self):
        return '<ID Wine {}>'.format(self.id)
