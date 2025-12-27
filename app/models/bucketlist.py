"""BucketList model for storing bucket list information."""
from datetime import datetime
from app import db


class BucketList(db.Model):
    """BucketList model for storing bucket list details."""
    
    __tablename__ = 'bucketlists'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('Item', backref='bucketlist', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, name, created_by):
        """Initialize bucketlist with name and creator."""
        self.name = name
        self.created_by = created_by
    
    def to_dict(self):
        """Convert bucketlist object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.to_dict() for item in self.items.all()],
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_modified': self.date_modified.isoformat() if self.date_modified else None,
            'created_by': str(self.created_by)
        }
    
    def __repr__(self):
        return f'<BucketList {self.name}>'