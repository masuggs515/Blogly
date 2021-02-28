"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

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

    users = User.query.order_by(User.last_name).all()
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

    new_user = User(first_name=first_name, last_name=last_name, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show details of user. Image and full name."""

    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Populate form to edit user information."""

    user = User.query.get_or_404(user_id)
    return render_template('edit_form.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Receive input and update database with new user details. If blank change nothing."""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    user = User.query.get_or_404(user_id)
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
    delete_user = User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')



