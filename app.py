"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, Users, Posts, Tags, PostTags

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """Route to home page."""

    return redirect('/users')

@app.route('/users')
def users_list():
    """Create and populate list of added users."""

    users = Users.query.order_by(Users.last_name).all()
    return render_template('list.html', users=users)

@app.route('/users/new')
def add_user_form():
    """Add a new user to database form."""

    return render_template('add_user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Receive client input for new user and add to database."""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]
    img_url = img_url if img_url else None

    new_user = Users(first_name=first_name, last_name=last_name, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show details of user. Image and full name."""

    user = Users.query.get_or_404(user_id)
    posts = Posts.query.filter_by(user_id=user_id).all()
    return render_template('details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Populate form to edit user information."""

    user = Users.query.get_or_404(user_id)
    return render_template('edit_user_form.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Receive input and update database with new user details. If blank change nothing."""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    user = Users.query.get_or_404(user_id)
    if first_name != '':
        user.first_name = first_name
    if last_name != '':
        user.last_name = last_name
    if img_url != '':
        user.image_url = img_url
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user and redirect to users list."""
    delete_user = Users.query.get_or_404(user_id)
    db.session.delete(delete_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Form to add a new post connected to user."""
    user = Users.query.get_or_404(user_id)
    tags = Tags.query.all()
    return render_template('post_form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_post(user_id):
    """Submit post to database."""
    title = request.form["title"]
    content = request.form["content"]
    added_tags = request.form.getlist("tags")

    tag_ids = []
    for num in added_tags:
        if num != '':
            tag_ids.append(int(num))

    tags = Tags.query.filter(Tags.id.in_(tag_ids)).all()    

    user = Users.query.get_or_404(user_id)
    new_post = Posts(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    post = Posts.query.get_or_404(new_post.id)
    for tag in tags:
        post_tag = PostTags(tag_id=tag.id, post_id=post.id)
        db.session.add(post_tag)
        db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Populate the post when it is clicked on."""
    post = Posts.query.get_or_404(post_id)
    return render_template('show_post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Form to edit post."""
    post = Posts.query.get_or_404(post_id)
    tags = Tags.query.all()
    return render_template('edit_post_form.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_post_edit(post_id):
    """Submit post edit to database."""
    title = request.form["title"]
    content = request.form["content"]
    added_tags = request.form.getlist("tags")

    old_tags = PostTags.query.filter_by(post_id=post_id).all()
    for tag in old_tags:
        db.session.delete(tag)
        db.session.commit()

    tag_ids = []
    for num in added_tags:
        if num != '':
            tag_ids.append(int(num))
            
    tags = Tags.query.filter(Tags.id.in_(tag_ids)).all() 

    post = Posts.query.get_or_404(post_id)
    

    post.title = title
    post.content = content
    db.session.commit()

    for tag in tags:
        post_tag = PostTags(tag_id=tag.id, post_id=post.id)
        db.session.add(post_tag)
        db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post from database."""
    post = Posts.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/tags')
def show_tags():
    tags = Tags.query.all()

    return render_template('tag_list.html', tags=tags)

@app.route('/tags/<tag_id>')
def tag_details(tag_id):
    tag = Tags.query.get_or_404(tag_id)

    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new')
def tag_form():

    return render_template('new_tag_form.html')

@app.route('/tags/new', methods=["POST"])
def submit_tag_form():
    tag_name = request.form["tag_name"]
    new_tag = Tags(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tags.query.get_or_404(tag_id)
    
    return render_template('tag_edit_form.html', tag=tag)

@app.route('/tags/<tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    tag_name = request.form["tag_name"]

    tag = Tags.query.get_or_404(tag_id)
    if tag_name != '':
        tag.name = tag_name
    db.session.commit()
    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tags.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.commit()
    return redirect('/tags')