import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app, db
from models import Episode, Guest, Appearance

def test_episode_creation():
    with app.app_context():
        episode = Episode(date="1/11/99", number=1)
        assert episode.date == "1/11/99"
        assert episode.number == 1

def test_guest_creation():
    with app.app_context():
        guest = Guest(name="Test", occupation="actor")
        assert guest.name == "Test"
        assert guest.occupation == "actor"

def test_rating_validation():
    with app.app_context():
        with pytest.raises(ValueError):
            appearance = Appearance(rating=6, episode_id=1, guest_id=1)

def test_cascade_delete(client, sample_data):
    with app.app_context():
        episode_id = sample_data['episode'].id
        episode = Episode.query.get(episode_id)
        
        db.session.delete(episode)
        db.session.commit()
        
        appearances = Appearance.query.filter_by(episode_id=episode_id).all()
        assert len(appearances) == 0
