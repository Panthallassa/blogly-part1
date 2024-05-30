"""Models for Blogly."""
from sqlalchemy import func
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