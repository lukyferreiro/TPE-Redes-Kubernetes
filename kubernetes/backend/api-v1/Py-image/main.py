from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from marshmallow import Schema, fields
from flask_cors import CORS
import os

app = Flask(__name__)

database_user = os.environ["POSTGRES_USER"]
database_password = os.environ["POSTGRES_PASS"]
database_db = os.environ["POSTGRES_DB"]
database_host = os.environ["POSTGRES_HOST"]

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{database_user}:{database_password}@{database_host}/{database_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    
    legajo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Movie %r>' % self.name

class AlumnosSchema(Schema):
    legajo = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)

@app.route("/")
def hello_world():

    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')