"""Blogly application."""

from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)
debug = DebugToolbarExtension(app)
app.app_context().push()
db.create_all()


@app.route('/')
def start_page():
    """Lists all of the Users"""
    users = User.query.all()
    return render_template('base.html', users=users)

@app.route('/users', methods=["GET"])
def user_page():
    """Lists all of the Users"""
    users = User.query.all()
    return render_template('base.html', users=users)

@app.route('/users/new', methods=["GET"])
def show_form():
    """Shows add user form"""
    return render_template('form.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Adds a new user to the database"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('user_page'))

@app.route('/users/<int:user_id>', methods=["GET"])
def show_user_page(user_id):
    """Shows a user details page"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["GET"])
def show_edit_page(user_id):
    """Shows user edit page"""
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Processes the submitted edit form"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()
    return redirect(url_for('user_page'))


@app.route('/users/<int:user_id>/delete', methods=["POST", "GET"])
def delete_user(user_id):
    """Deletes the user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_page'))


@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def new_post(user_id):
    """Adds a new post"""
    user = User.query.get_or_404(user_id)
    return render_template('post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_post(user_id):
    """Handles the submission of a post"""
    title = request.form['title']
    content = request.form['content']

    if not title or not content:
        flash('Title and content required.', 'error')
        return redirect(url_for('new_post', user_id=user_id))
    
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('show_user_page', user_id=user_id))


@app.route('/posts/<int:post_id>', methods=["GET", "POST"])
def show_post(post_id):
    """Shows the post of given id"""
    print("Fetching post with ID:", post_id)
    post = Post.query.get_or_404(post_id)
    print("Post found:", post)
    return render_template('post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def edit_post(post_id):
    """Shows editing page for a post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Update a post"""
    title = request.form['title']
    content = request.form['content']

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content

    db.session.commit()

    return redirect(url_for('show_post', post_id=post.id))

@app.route('/posts/<int:post_id>/delete', methods=['POST', 'GET'])
def delete_post(post_id):
    """Deletes a post from the database and UI"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('user_page'))