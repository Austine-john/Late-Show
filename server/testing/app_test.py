import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

def test_get_episodes(client, sample_data):
    response = client.get('/episodes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0

def test_get_episode_success(client, sample_data):
    episode_id = sample_data['episode'].id
    response = client.get(f'/episodes/{episode_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'appearances' in data

def test_get_episode_not_found(client):
    response = client.get('/episodes/9999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_delete_episode_success(client, sample_data):
    episode_id = sample_data['episode'].id
    response = client.delete(f'/episodes/{episode_id}')
    assert response.status_code == 204

def test_delete_episode_not_found(client):
    response = client.delete('/episodes/9999')
    assert response.status_code == 404

def test_get_guests(client, sample_data):
    response = client.get('/guests')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0

def test_create_appearance_success(client, sample_data):
    data = {
        'rating': 5,
        'episode_id': sample_data['episode'].id,
        'guest_id': sample_data['guest'].id
    }
    response = client.post('/appearances', 
                          data=json.dumps(data),
                          content_type='application/json')
    assert response.status_code == 201

def test_create_appearance_invalid_rating(client, sample_data):
    data = {
        'rating': 10,
        'episode_id': sample_data['episode'].id,
        'guest_id': sample_data['guest'].id
    }
    response = client.post('/appearances',
                          data=json.dumps(data),
                          content_type='application/json')
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'errors' in result
