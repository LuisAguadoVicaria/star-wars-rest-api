import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Routes
@app.route('/planets', methods=['GET'])
def planets_all():
    pl = Planets.query.all()
    return jsonify([x.to_dict() for x in pl]), 200

@app.route('/characters', methods=['GET'])
def characters_all():
    ch = Characters.query.all()
    return jsonify([x.to_dict() for x in ch]), 200

@app.route('/users', methods=['GET'])
def users_all():
    users = User.query.all()
    return jsonify([x.to_dict() for x in users]), 200


@app.route('/users/<int:u_id>', methods=['GET'])
def user_single(u_id):
    user = User.query.get(u_id)
    return jsonify(user.to_dict()), 200

@app.route('/users/<int:u_id>/favorites', methods=['GET'])
def all_favorites(u_id):
    user1 = User.query.get(u_id)
    user1.to_dict()
    ret = {"fv_planets": user1.fav_planets, "fv_characters": user1.fav_characters}
    return jsonify(ret), 200

@app.route('/users/<int:u_id>/favorites/planet/<int:planet_id>', methods=['PUT', 'DELETE'])
def planets_favorites(u_id):
    body = request.get_json() #{ 'username': 'new_username'}
    if request.method == 'PUT':
        user1 = User.query.get(u_id)
        planet = Planets.query.get(planet_id)
        user1.fav_planets.append(planet)
        db.session.commit()
        return "Added Planet fav", 200
    if request.method == 'DELETE':
        user1 = User.query.get(u_id)
        planet = Planets.query.get(planet_id)
        user1.fav_planets.remove(planet)
        db.session.commit()
        return "Deleted Planet Fav"
    return "Invalid Method", 404

@app.route('/users/<int:u_id>/favorites/character/<int:character_id>', methods=['PUT', 'DELETE'])
def characters_favorites(u_id):
    body = request.get_json() #{ 'username': 'new_username'}
    if request.method == 'PUT':
        user1 = User.query.get(u_id)
        character = Characters.query.get(character_id)
        user1.fav_characters.append(character)
        db.session.commit()
        return "Added Character fav", 200
    if request.method == 'DELETE':
        user1 = User.query.get(u_id)
        character = Characters.query.get(character_id)
        user1.fav_characters.remove(character)
        db.session.commit()
        return "Deleted Character Fav"
    return "Invalid Method", 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
