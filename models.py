"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# SCHEMA for blogly

# log in/sign up schema

class User(db.Model):
    """Template for user table"""

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f'<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(14),
                    nullable=False)
    last_name = db.Column(db.String(14),
                    nullable=False)
    image_url = db.Column(db.String(999),
                    default='https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg')

    
    def get_full_name(self):
        """Combine first and last names to populate full name."""
        return f'{self.first_name} {self.last_name}'