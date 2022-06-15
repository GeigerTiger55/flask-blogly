"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.get('/')
def show_users():
    """Shows the list of existing users"""

    users = User.query.all()
    return render_template('user_listing.html', users=users)


@app.get('/users/new')
def add_user_form():
    """Loads form to enter new user data"""
    return render_template('create_user.html')

@app.post('/users/new')
def create_user():
    """Creates new user from form data"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = URL(image_url) if image_url else None

    """CREATE INSTANCE OF USER"""
    user = User(
        first_name=first_name, 
        last_name=last_name, 
        image_url=image_url,
        )
    
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.get('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show information about a single user"""

    user = User.query.get_or_4040(user_id)
    return render_template("user_detail.html", user=user)