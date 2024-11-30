from app import create_app, db
from app.models import User, Activity, Challenge, ForumPost, Comment, Event, Product
from datetime import datetime, timedelta

def init_db():
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("Dropped all existing tables.")
        
        # Create all tables
        db.create_all()
        print("Created all tables successfully.")
        
        # Create a test user
        test_user = User(
            username="test_user",
            email="test@example.com"
        )
        test_user.set_password("password123")
        db.session.add(test_user)
        
        # Create an admin user
        admin_user = User(
            username="admin",
            email="admin@example.com"
        )
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        
        # Create some sample activities
        activities = [
            Activity(
                user_id=1,
                category="Transportation",
                description="Cycled to work instead of driving",
                impact=-2.5,
                date=datetime.utcnow() - timedelta(days=2)
            ),
            Activity(
                user_id=1,
                category="Energy",
                description="Installed LED bulbs",
                impact=-1.2,
                date=datetime.utcnow() - timedelta(days=1)
            ),
            Activity(
                user_id=1,
                category="Food",
                description="Had a meatless day",
                impact=-3.6,
                date=datetime.utcnow()
            )
        ]
        db.session.add_all(activities)
        
        # Create some challenges
        challenges = [
            Challenge(
                title="30 Days No Car",
                description="Challenge yourself to use alternative transportation for 30 days! Walk, bike, or take public transit to reduce your carbon footprint. Track your progress and share your experiences with the community.",
                category="Transportation",
                difficulty="Hard",
                points=1000,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=30)
            ),
            Challenge(
                title="Zero Waste Week",
                description="Can you go an entire week without producing landfill waste? Learn about composting, recycling, and waste reduction strategies. Document your journey and inspire others!",
                category="Waste",
                difficulty="Medium",
                points=500,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=7)
            ),
            Challenge(
                title="Plant-Based Diet Challenge",
                description="Try eating a plant-based diet for two weeks! Discover new recipes, reduce your carbon footprint, and experience the health benefits of plant-based eating.",
                category="Food",
                difficulty="Medium",
                points=750,
                start_date=datetime.utcnow() + timedelta(days=7),
                end_date=datetime.utcnow() + timedelta(days=21)
            ),
            Challenge(
                title="Energy Saving Sprint",
                description="Reduce your energy consumption by 20% in just 5 days! Learn about energy-efficient practices, monitor your usage, and compete with others to save the most energy.",
                category="Energy",
                difficulty="Easy",
                points=250,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=5)
            )
        ]
        db.session.add_all(challenges)
        
        # Create some forum posts
        posts = [
            ForumPost(
                user_id=1,
                title="Tips for Reducing Plastic Use",
                content="Share your best tips for reducing plastic consumption in daily life. I've started bringing my own bags to the grocery store and using reusable water bottles. What are your strategies?",
                category="Tips"
            ),
            ForumPost(
                user_id=1,
                title="Local Clean-up Event",
                content="Organizing a beach clean-up this weekend at Ocean Beach. Looking for volunteers! We'll provide gloves and bags. Let's make a difference in our community!",
                category="Events"
            ),
            ForumPost(
                user_id=2,
                title="Success Story: Solar Panel Installation",
                content="Just installed solar panels on my roof and wanted to share my experience. The process was surprisingly smooth, and I'm already seeing savings on my energy bill!",
                category="Success Stories"
            )
        ]
        db.session.add_all(posts)
        
        # Add some comments
        comments = [
            Comment(
                user_id=2,
                post_id=1,
                content="Great tips! I've also started using beeswax wraps instead of plastic wrap. They work really well!"
            ),
            Comment(
                user_id=1,
                post_id=3,
                content="That's amazing! I've been considering solar panels too. Would love to hear more about the installation process."
            )
        ]
        db.session.add_all(comments)
        
        # Commit all changes
        db.session.commit()
        print("Added sample data successfully.")

if __name__ == "__main__":
    init_db()
