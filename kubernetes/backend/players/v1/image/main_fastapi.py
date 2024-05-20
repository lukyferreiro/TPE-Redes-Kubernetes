from os import getenv
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .db import Base

load_dotenv()

PG_USER = getenv("POSTGRES_USER", "user")
PG_PASSWORD = getenv("POSTGRES_PASSWORD", "password")
PG_HOST = getenv("POSTGRES_HOST", "localhost")
PG_PORT = getenv("POSTGRES_PORT", 5432)
PG_DB = getenv("POSTGRES_DB", "db")

SQLALCHEMY_DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    age = Column(Integer, nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kgs = Column(Float, nullable=False)

    def __repr__(self):
        return '<Player %r>' % self.name

class PlayerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    height_cm = fields.Float(required=True)
    weight_kgs = fields.Float(required=True)


app = FastAPI()

def _get_response_headers():
    return {
        'X-POD-IP': getenv('POD_IP'),
        'X-POD-NAME': getenv('POD_NAME'),
        'X-NODE-NAME': getenv('NODE_NAME'),
    }

@app.get("/")
async def root(response: Response):
    specs = {
        "players_url": "http://api.players.com/v1/players?name={name}{&size}",
    }
    
    response.headers.update(_get_response_headers())
    return specs

@app.get("/players")
async def players(response: Response, db: Session = Depends(get_db)):
    response.headers.update(_get_response_headers())
    return db.query(Player).limit(10).all()


@app.get("/players/{id}")
async def player_by_id(response: Response, id: int, db: Session = Depends(get_db)):
    response.headers.update(_get_response_headers())
    player = db.query(Player).get(id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


if __name__ == "__main__":
    port = getenv("FASTAPI_PORT", 8000)
    try:
        port = int(port)
    except ValueError:
        port = 8000

    uvicorn.run(app, host="0.0.0.0", port=port)
