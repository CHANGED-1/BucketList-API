"""Unit tests for models."""
import unittest
from app import create_app, db
from app.models import User, BucketList, Item


class ModelsTestCase(unittest.TestCase):
    """Test case for models."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_password_hashing(self):
        """Test password hashing."""
        user = User(email='test@test.com', username='testuser', password='password')
        self.assertNotEqual(user.password_hash, 'password')
        self.assertTrue(user.check_password('password'))
        self.assertFalse(user.check_password('wrongpassword'))
    
    def test_bucketlist_creation(self):
        """Test bucket list creation."""
        user = User(email='test@test.com', username='testuser', password='password')
        db.session.add(user)
        db.session.commit()
        
        bucketlist = BucketList(name='Test List', created_by=user.id)
        db.session.add(bucketlist)
        db.session.commit()
        
        self.assertEqual(bucketlist.name, 'Test List')
        self.assertEqual(bucketlist.created_by, user.id)
    
    def test_item_creation(self):
        """Test item creation."""
        user = User(email='test@test.com', username='testuser', password='password')
        db.session.add(user)
        db.session.commit()
        
        bucketlist = BucketList(name='Test List', created_by=user.id)
        db.session.add(bucketlist)
        db.session.commit()
        
        item = Item(name='Test Item', bucketlist_id=bucketlist.id)
        db.session.add(item)
        db.session.commit()
        
        self.assertEqual(item.name, 'Test Item')
        self.assertFalse(item.done)


if __name__ == '__main__':
    unittest.main()