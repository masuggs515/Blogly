from unittest import TestCase
from app import app
from flask import session
from models import User, db


class FlaskTests(TestCase):

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()

    def tearDown(self):
        """Clean up any issued query"""

        db.session.rollback()

    def test_get_full_name(self):
        user = User(first_name='John', last_name='Stamos')
        self.assertEquals(user.get_full_name(), "John Stamos")

    def test_users_list(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>List of Users</h1>' , html)

    def test_add_user_form(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Add a User</h1>' , html)