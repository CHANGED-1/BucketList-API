"""Integration tests for API endpoints."""
import unittest
import json
from app import create_app, db
from app.models import User


class APITestCase(unittest.TestCase):
    """Test case for API endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def register_user(self, email='test@test.com', username='testuser', password='password'):
        """Helper method to register a user."""
        return self.client.post(
            '/api/v1/auth/register',
            data=json.dumps({
                'email': email,
                'username': username,
                'password': password
            }),
            content_type='application/json'
        )
    
    def login_user(self, username='testuser', password='password'):
        """Helper method to login a user."""
        return self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'username': username,
                'password': password
            }),
            content_type='application/json'
        )
    
    def test_registration(self):
        """Test user registration."""
        response = self.register_user()
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertIn('user', data)
    
    def test_login(self):
        """Test user login."""
        self.register_user()
        response = self.login_user()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)
    
    def test_create_bucketlist(self):
        """Test bucket list creation."""
        # Register and login
        self.register_user()
        login_response = self.login_user()
        token = json.loads(login_response.data)['token']
        
        # Create bucket list
        response = self.client.post(
            '/api/v1/bucketlists',
            data=json.dumps({'name': 'My Bucket List'}),
            headers={'Authorization': f'Bearer {token}'},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['bucketlist']['name'], 'My Bucket List')
    
    def test_get_bucketlists(self):
        """Test getting bucket lists."""
        # Register and login
        self.register_user()
        login_response = self.login_user()
        token = json.loads(login_response.data)['token']
        
        # Create bucket lists
        for i in range(3):
            self.client.post(
                '/api/v1/bucketlists',
                data=json.dumps({'name': f'List {i}'}),
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json'
            )
        
        # Get bucket lists
        response = self.client.get(
            '/api/v1/bucketlists',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['bucketlists']), 3)
    
    def test_pagination(self):
        """Test pagination."""
        # Register and login
        self.register_user()
        login_response = self.login_user()
        token = json.loads(login_response.data)['token']
        
        # Create 25 bucket lists
        for i in range(25):
            self.client.post(
                '/api/v1/bucketlists',
                data=json.dumps({'name': f'List {i}'}),
                headers={'Authorization': f'Bearer {token}'},
                content_type='application/json'
            )
        
        # Get first page with limit 10
        response = self.client.get(
            '/api/v1/bucketlists?limit=10&page=1',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        data = json.loads(response.data)
        self.assertEqual(len(data['bucketlists']), 10)
        self.assertEqual(data['total'], 25)
        self.assertEqual(data['pages'], 3)
    
    def test_search(self):
        """Test search functionality."""
        # Register and login
        self.register_user()
        login_response = self.login_user()
        token = json.loads(login_response.data)['token']
        
        # Create bucket lists
        self.client.post(
            '/api/v1/bucketlists',
            data=json.dumps({'name': 'Travel Goals'}),
            headers={'Authorization': f'Bearer {token}'},
            content_type='application/json'
        )
        self.client.post(
            '/api/v1/bucketlists',
            data=json.dumps({'name': 'Career Goals'}),
            headers={'Authorization': f'Bearer {token}'},
            content_type='application/json'
        )
        
        # Search for 'travel'
        response = self.client.get(
            '/api/v1/bucketlists?q=travel',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        data = json.loads(response.data)
        self.assertEqual(len(data['bucketlists']), 1)
        self.assertIn('Travel', data['bucketlists'][0]['name'])


if __name__ == '__main__':
    unittest.main()