"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# SCHEMA for blogly

# log in/sign up schema
DEFAULT_IMAGE = 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg'

class Users(db.Model):
    """Template for user table"""

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f'<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(25),
                    nullable=False)
    last_name = db.Column(db.String(25),
                    nullable=False)
    image_url = db.Column(db.Text,
                    default=DEFAULT_IMAGE)

    post = db.relationship("Posts", cascade="all, delete-orphan", backref="user")
    
    def get_full_name(self):
        """Combine first and last names to populate full name."""
        return f'{self.first_name} {self.last_name}'

class Posts(db.Model):
    """Template for posts table."""

    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f'<Post title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}>'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(40),
                    nullable=False)
    content = db.Column(db.Text,
                    nullable=False)
    created_at = db.Column(db.Date,
                    default=datetime.now())
    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id'))

class Tags(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(15),
                    unique=True,
                    nullable=False)

    post = db.relationship("Posts", secondary="post_tag", backref="tags")

class PostTags(db.Model):
    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
                
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key=True
                        )