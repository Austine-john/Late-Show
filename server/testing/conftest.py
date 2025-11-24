import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app, db
from models import Episode, Guest, Appearance

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        
        # Create sample data
        ep = Episode(date="1/11/99", number=1)
        guest = Guest(name="Test Guest", occupation="tester")
        db.session.add_all([ep, guest])
        db.session.commit()
        
        appearance = Appearance(rating=4, episode_id=ep.id, guest_id=guest.id)
        db.session.add(appearance)
        db.session.commit()
        
        yield app.test_client()
        db.drop_all()

@pytest.fixture
def sample_data(client):
    with app.app_context():
        # Return IDs instead of objects to avoid detached instance errors
        episode = Episode.query.first()
        guest = Guest.query.first()
        return {
            'episode': episode,
            'guest': guest,
            'appearance': Appearance.query.first()
        }
