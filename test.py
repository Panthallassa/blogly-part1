import unittest
from app import app, db
from models import User, Post

class TestApp(unittest.TestCase):
    def setUp(self):
        """Set up the test client"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

            # add a sample user
            user = User(first_name='Test', last_name='User', image_url='http://example.com/user.jpg')
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        """Tear down the test client"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # def test_user_page(self):
    #     """Test the user_page route"""
    #     response = self.client.get('/users')
    #     self.assertEqual(response.status_code, 200)

    # def test_add_new_user(self):
    #     """Testm the add_new_user route"""
    #     data = {'first_name': 'John', 'last_name': 'Doe', 'image_url': 'example.com'}
    #     response = self.client.post('/users/new', data=data)
    #     self.assertEqual(response.status_code, 302)

    # def test_update_user(self):
    #     """Test the update_user route"""
    #     user = User(first_name='John', last_name='Doe', image_url='example.com')
    #     db.session.add(user)
    #     db.session.commit()

    #     data = {'first_name': 'Jane', 'last_name': 'Doe', 'image_url': 'example.com'}
    #     response = self.client.post(f'/users/{user.id}/edit', data=data)

    #     updated_user = User.query.get(user.id)
    #     self.asserEqual(updated_user.first_name, 'Jane')

    # def test_delete_user(self):
    #     """Test the delete_user route"""
    #     user = User(first_name='John', last_name='Doe', image_url='example.com')
    #     db.session.add(user)
    #     db.session.commit()

    #     response = self.client.post(f'/users/{user.id}/delete')

    #     deleted_user = User.query.get(user.id)
    #     self.assertIsNone(deleted_user)

    def test_new_post_get(self):
        """Test the new post form page loads correctly"""
        response = self.client.get(f'/users/{self.user_id}/posts/new')
        self.assertEqual(response.status_code, 200)
        self.assertin(b'Add a new post', response.data)

    def test_submit_post(self):
        """Test submitting a new post"""
        response = self.client.post(f'/users/{self.user_id}/posts/new', data={
            'title': 'Test Post',
            'content': 'This is a test post.'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)

    def test_show_post(self):
        """Test showing a specific post"""
        with app.app_context():
            post = Post(title='Test Post', content='Test Content', user_id=self.user_id)
            db.session.add(post)
            db.session.commit()

            response = self.client.get(f'/post/{post.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Post', response.data)
            self.asserIn(b'Test Content', response.data)

    def test_edit_post_get(self):
        """Test the edit post form page loads correctly"""
        with app.app_context():
            post = Post(title='Test Post', content='Test Content', user_id=self.user_id) 
            db.session.add(post)
            db.session.commit()

            response = self.client.get(f'/posts/{post.id}/edit')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Edit Post', response.data)

    def test_update_post(self):
        """Test updating a post"""
        with app.app_context():
            post = Post(title='Test Post', content='Test Content', user_id=self.user_id)
            db.session.add(post)
            db.session.commit()

            response = self.client.post(f'/posts/{post.id}/edit', data={
                'title': 'Updated Title',
                'content': 'Updated Content'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Updated Title', response.data)
            self.assertIn(b'Updated Content', response.data)

    def test_delete_post(self):
        """Test deleting a post"""
        with app.app_context():
            post = Post(title='Test Post', content='Test Content', user_id=self.user_id)
            db.session.add(post)
            db.session.commit()

            response = self.client.post(f'/posts/{post.id}/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'Test Post', response.data)
            