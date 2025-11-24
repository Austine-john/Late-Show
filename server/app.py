from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Late Show API</h1>'

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([{
        'id': e.id,
        'date': e.date,
        'number': e.number
    } for e in episodes]), 200

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404
    
    return jsonify(episode.to_dict()), 200

@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404
    
    db.session.delete(episode)
    db.session.commit()
    return '', 204

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([{
        'id': g.id,
        'name': g.name,
        'occupation': g.occupation
    } for g in guests]), 200

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    
    try:
        appearance = Appearance(
            rating=data.get('rating'),
            episode_id=data.get('episode_id'),
            guest_id=data.get('guest_id')
        )
        db.session.add(appearance)
        db.session.commit()
        
        return jsonify(appearance.to_dict()), 201
    except ValueError as e:
        return jsonify({'errors': [str(e)]}), 400
    except Exception as e:
        return jsonify({'errors': ['validation errors']}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
