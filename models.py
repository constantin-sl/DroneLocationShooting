from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Объект локации
class LocationObj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    coords = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer, default=0, nullable=True)

    def __repr__(self):
        return f"LocationObj(name='{self.name}', coords='{self.coords}', status='{self.status}')"
