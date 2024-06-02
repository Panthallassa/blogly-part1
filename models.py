"""Models for Blogly."""
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50), 
                           nullable=False)
    last_name = db.Column(db.String(50), 
                          nullable=False)
    image_url = db.Column(db.String(255))

    posts = db.relationship('Post', 
                            back_populates='user', 
                            cascade='all, delete-orphan')
    

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(25),
                      nullable=False)
    content = db.Column(db.String,
                        nullable=False)
    created_at = db.Column(db.DateTime, 
                           default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='posts')
    tags = db.relationship('Tag', secondary='post_tags', back_populates='posts')


class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.Text,
                     nullable=False, 
                     unique=True)
    
    posts = db.relationship('Post', secondary='post_tags', back_populates='tags')
    

class PostTag(db.Model):

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable=False)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)


