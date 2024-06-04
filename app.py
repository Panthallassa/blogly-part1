"""Blogly application."""

from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, connect_db, User, Post, Tag
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
    tags = Tag.query.all()
    
    return render_template('post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_post(user_id):
    """Handles the submission of a post"""
    title = request.form['title']
    content = request.form['content']
    tag_ids = request.form.getlist('tags')

    if not title or not content:
        flash('Title and content required.', 'error')
        return redirect(url_for('new_post', user_id=user_id))
    
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        new_post.tags = tags
        db.session.commit()

    return redirect(url_for('show_user_page', user_id=user_id))


@app.route('/posts/<int:post_id>', methods=["GET", "POST"])
def show_post(post_id):
    """Shows the post of given id"""
    post = Post.query.get_or_404(post_id)
    tags = post.tags

    return render_template('post_details.html', post=post, tags=post.tags)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Shows editing page for a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        tag_ids = request.form.getlist('tags')
        post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        db.session.commit()
        return redirect(url_for('show_post', post_id=post.id))
    return render_template('post_edit.html', post=post, tags=tags)

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

@app.route('/tags', methods=["GET"])
def show_tags():
    """Shows a list of all tags"""
    tags = Tag.query.all()
    return render_template('list_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Shows one specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)

@app.route('/tags/new', methods=["GET"])
def add_tag():
    """Route to add a new tag"""
    return render_template('add_tag.html')

@app.route('/tags/new', methods=["POST"])
def commit_tag():
    """Add a tag to the database"""
    tag_name = request.form['add-tag']
    tag = Tag(name=tag_name)
    db.session.add(tag)
    db.session.commit()
    return redirect(url_for('show_tags'))

@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def edit_tag(tag_id):
    """Shows editing page for a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def post_edit_tag(tag_id):
    """Adds updates to the database"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['add-tag']
    db.session.add(tag)
    db.session.commit()
    return redirect(url_for('show_tags'))

@app.route('/tags/<int:tag_id>/delete', methods=["GET", "POST"])
def delete_tag(tag_id):
    """Deletes a tag of given tag_id"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect(url_for('show_tags'))

if __name__ == '__main__':
    app.run(debug=True)
