from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from marshmallow import Schema, fields
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app, expose_headers='*')   #Configura CORS para permitir solicitudes de origen cruzado desde cualquier dominio

database_user = os.environ["POSTGRES_USER"]
database_password = os.environ["POSTGRES_PASS"]
database_db = os.environ["POSTGRES_DB"]
database_host = os.environ["POSTGRES_HOST"]
database_port = os.environ["POSTGRES_PORT"]

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{database_user}:{database_password}@{database_host}/{database_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#----------------------------------------------
#---------------Model and Schema---------------
#----------------------------------------------

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kgs = db.Column(db.Float, nullable=False)
    positions = db.Column(db.Text, nullable=False)
    nationality = db.Column(db.Text, nullable=False)
    overall_rating = db.Column(db.Integer, nullable=False)
    potential = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Player %r>' % self.name

class PlayerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    full_name = fields.Str(required=True)
    age = fields.Int(required=True)
    height_cm = fields.Float(required=True)
    weight_kgs = fields.Float(required=True)
    positions = fields.Str(required=True)
    nationality = fields.Str(required=True)
    overall_rating = fields.Int(required=True)
    potential = fields.Int(required=True)


#----------------------------------------------
#------------------Endpoints-------------------
#----------------------------------------------

def _get_response_headers():
    return {
        'X-NODE-NAME': os.environ.get('NODE_NAME'),
        'X-NODE-IP': os.environ.get('NODE_IP'),
        'X-POD-IP': os.environ.get('POD_IP'),
        'X-POD-NAME': os.environ.get('POD_NAME'),
        'X-POD-NAMESPACE': os.environ.get('POD_NAMESPACE'),
        'X-POD-UID': os.environ.get('POD_UID'),
        'X-POD-SERVICE-ACCOUNT': os.environ.get('POD_SERVICE_ACCOUNT'),
    }

@app.route('/', methods=['GET'])
def get_api_specification():
    specs = {
        "players_url": "http://api.players.com/v2/players?name={name}{&size}",
        "player_url": "http://api.players.com/v2/players/{id}",
        #"db_url": f"postgresql://{database_user}:{database_password}@{database_host}/{database_db}"
    }

    response = make_response(specs, 200)
    response.headers.extend(_get_response_headers())

    return response

@app.route('/players', methods=['GET'])
def get_players():
    name = request.args.get('name')
    size = request.args.get('size', default=5, type=int)

    if not name:
        response = jsonify({'error': 'Missing name parameter'})
        response.status_code = 400
        response.headers.extend(_get_response_headers())
        return response

    players = Player.query.filter(or_(*[Player.name.ilike('%{}%'.format(token)) for token in name.split()])).all()

    players = players[:size]

    schema = PlayerSchema(many=True)
    serialized_players = schema.dump(players)

    response = make_response(serialized_players, 200)
    response.headers.extend(_get_response_headers())
    
    return response

@app.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.query.get(player_id)

    if not player:
        response = jsonify({'error': 'Player not found'})
        response.status_code = 404
        response.headers.extend(_get_response_headers())
        return response

    schema = PlayerSchema()
    serialized_player = schema.dump(player)

    response = make_response(serialized_player, 200)
    response.headers.extend(_get_response_headers())
    
    return response

if __name__ == '__main__':
    #Se inicia el servidor Flask en el puerto 8080 y escucha en todas las interfaces
    app.run(debug=True, port=8080, host='0.0.0.0')
