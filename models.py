"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://thumbs.dreamstime.com/b/default-avatar-profile-image-vector-social-media-user-icon-potrait-182347582.jpg'

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column( 
        db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column( 
        db.String(50),
        nullable=False)
    last_name = db.Column(  
        db.String(50),
        nullable=False)
    image_url = db.Column(  
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL)


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column( 
        db.Integer,
        primary_key=True,
        autoincrement=True)
    title = db.Column(
        db.String(100),
        nullable=False)
    content = db.Column(
        db.Text,
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now())
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')
    