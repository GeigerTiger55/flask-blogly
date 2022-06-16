"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
#db.drop_all()
db.create_all()


@app.get('/')
def homepage_redirect():
    """redirects to user page"""

    return redirect('/users')


@app.get('/users')
def show_users():
    """Shows the list of existing users"""

    users = User.query.all()
    return render_template('user_listing.html', users=users)


@app.get('/users/new')
def show_add_user_form():
    """Loads form to enter new user data"""
    return render_template('user_create.html')


@app.post('/users/new')
def create_user():
    """Creates new user from form data"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

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
    """Show information about a single user
        TODO: add handling for 404
    """

    user = User.query.get_or_404(user_id)
    posts = user.posts

    return render_template("user_detail.html", user=user, posts=posts)


@app.get('/users/<int:user_id>/edit')
def show_user_edit_form(user_id):
    """Show form to edit user information"""

    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)


@app.post('/users/<int:user_id>/edit')
def save_user_edits(user_id):
    """Saves user updates and redirect to user list"""

    # check for no updates and return orginal value
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else DEFAULT_IMAGE_URL

    user = User.query.get(user_id) 

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()
    
    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user_info(user_id):
    """Deletes user from database"""
    
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    """Render the add post form"""

    user = User.query.get(user_id)

    return render_template('post_create.html', user=user)


@app.post('/users/<int:user_id>/posts/new')
def create_post(user_id):
    """Render the add post form"""
    
    title = request.form['title']
    content = request.form['content']

    post = Post(
        title=title,
        content=content,
        user_id=user_id
    )

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.get('/posts/<int:post_id>')
def show_post_detail(post_id):
    """Show post.
        TODO: add handling for 404
    """

    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template("post_detail.html", user=user, post=post)


@app.get('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """Show form to edit post information"""

    post = Post.query.get_or_404(post_id)
    return render_template("post_edit.html", post=post)


@app.post("/posts/<int:post_id>/edit")
def save_post_edits(post_id):
    """Saves post updates and redirect to user page"""

    # check for no updates and return orginal value
    title = request.form['title']
    content = request.form['content']

    post = Post.query.get(post_id) 

    post.title = title
    post.content = content

    user_id = post.user_id

    db.session.commit()
    
    return redirect(f'/users/{ user_id }')


@app.post('/posts/<int:post_id>/delete')
def delete_post_info(post_id):
    """Deletes user from database"""
    
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{ user_id }')