"""Management script for database operations."""
import os
from flask_migrate import Migrate
from app import create_app, db

# Get environment or default to development
env = os.getenv("FLASK_ENV", "development")
app = create_app(env)

migrate = Migrate(app, db)


@app.cli.command("create-db")
def create_db():
    """Create database tables."""
    db.create_all()
    print("Database tables created successfully!")


@app.cli.command("drop-db")
def drop_db():
    """Drop all database tables."""
    if input("Are you sure you want to drop all tables? (yes/no): ").lower() == "yes":
        db.drop_all()
        print("Database tables dropped successfully!")
    else:
        print("Operation cancelled.")


@app.cli.command("seed-db")
def seed_db():
    """Seed database with sample data."""
    from app.models import User, BucketList, Item

    user = User(
        email="test@example.com",
        username="testuser",
        password="password123",
    )
    db.session.add(user)
    db.session.commit()

    bucketlist = BucketList(name="Travel Goals", created_by=user.id)
    db.session.add(bucketlist)
    db.session.commit()

    items = [
        Item(name="Visit Paris", bucketlist_id=bucketlist.id),
        Item(name="See Northern Lights", bucketlist_id=bucketlist.id),
        Item(
            name="Climb Mount Kilimanjaro",
            bucketlist_id=bucketlist.id,
            done=True,
        ),
    ]
    db.session.add_all(items)
    db.session.commit()

    print("Database seeded successfully!")
