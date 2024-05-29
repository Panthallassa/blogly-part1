import unittest
from app import app, db
from models import User

class TestApp(unittest.TestCase):
    def setUp(self):
        """Set up the test client"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test client"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_page(self):
        """Test the user_page route"""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_add_new_user(self):
        """Testm the add_new_user route"""
        data = {'first_name': 'John', 'last_name': 'Doe', 'image_url': 'example.com'}
        response = self.client.post('/users/new', data=data)
        self.assertEqual(response.status_code, 302)

    def test_update_user(self):
        """Test the update_user route"""
        user = User(first_name='John', last_name='Doe', image_url='example.com')
        db.session.add(user)
        db.session.commit()

        data = {'first_name': 'Jane', 'last_name': 'Doe', 'image_url': 'example.com'}
        response = self.client.post(f'/users/{user.id}/edit', data=data)

        updated_user = User.query.get(user.id)
        self.asserEqual(updated_user.first_name, 'Jane')

    def test_delete_user(self):
        """Test the delete_user route"""
        user = User(first_name='John', last_name='Doe', image_url='example.com')
        db.session.add(user)
        db.session.commit()

        response = self.client.post(f'/users/{user.id}/delete')

        deleted_user = User.query.get(user.id)
        self.assertIsNone(deleted_user)