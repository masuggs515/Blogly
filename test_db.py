from unittest import TestCase
from app import app
from models import db, User


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config["TESTING"] = True

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):

    def setUp(self):
        """Delete queries and add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="Test", image_url="Test")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up failed commits."""

        db.session.rollback()

    def test_users_list(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Test', html)

    def test_user_detail(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<h1>{self.user.get_full_name()} Details</h1>', html)