from unittest import TestCase
from app import app
from models import db, Users, Posts


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config["TESTING"] = True

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):

    def setUp(self):
        """Delete queries and add sample user."""

        Posts.query.delete()
        Users.query.delete()

        user = User(first_name="Test", last_name="Test", image_url="Test")
        db.session.add(user)
        db.session.commit()
        post = Post(title="Test", content="Test", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.user = user
        self.post = post
        self.post_id = post.id

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
            self.assertIn(f'<h4 class="d-inline text-center my-4">{self.user.get_full_name()}</h4>', html)


    def test_edit_post_form(self):
        with app.test_client() as client:
            res = client.get(f'/posts/{self.post_id}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<h2>Edit {self.post.title}</h2>', html)

    def test_add_user(self):
        with app.test_client() as client:
            sent = { "first_name": "Test2", "last_name": "Test2", "img_url": "Test2" }
            res = client.post('/users/new', data=sent, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<h1>List of Users</h1>', html)
            self.assertIn(f'Test2, Test2', html)

    def test_edit_user(self):
        with app.test_client() as client:
            sent = {"first_name": "Test2", "last_name": "Test2", "img_url": "Test2" }
            res = client.post(f'/users/{self.user_id}/edit', data=sent, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<h1>List of Users</h1>', html)
            self.assertIn(f'Test2, Test2', html)

    def test_delete_user(self):
        with app.test_client() as client:
            res = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<h1>List of Users</h1>', html)
            self.assertNotIn(f'Test, Test', html)