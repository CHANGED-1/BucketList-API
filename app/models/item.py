"""Item model for bucket list items."""
from datetime import datetime
from app import db


class Item(db.Model):
    """Item model for storing bucket list item details."""
    
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, bucketlist_id, done=False):
        """Initialize item with name and bucketlist."""
        self.name = name
        self.bucketlist_id = bucketlist_id
        self.done = done
    
    def to_dict(self):
        """Convert item object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_modified': self.date_modified.isoformat() if self.date_modified else None,
            'done': self.done
        }
    
    def __repr__(self):
        return f'<Item {self.name}>'