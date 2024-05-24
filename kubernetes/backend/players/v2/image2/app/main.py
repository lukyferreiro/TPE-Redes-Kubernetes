from os import getenv
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, Column, Integer, Text, Float
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

app = FastAPI()

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
    full_name = Column(Text, nullable=False)
    age = Column(Integer, nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kgs = Column(Float, nullable=False)
    positions = Column(Text, nullable=False)
    nationality = Column(Text, nullable=False)
    overall_rating = Column(Integer, nullable=False)
    potential = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Player %r>' % self.name

def _get_response_headers():
    return {
        'X-NODE-NAME': getenv('NODE_NAME'),
        'X-NODE-IP': getenv('NODE_IP'),
        'X-POD-IP': getenv('POD_IP'),
        'X-POD-NAME': getenv('POD_NAME'),
        'X-POD-NAMESPACE': getenv('POD_NAMESPACE'),
        'X-POD-UID': getenv('POD_UID'),
        'X-POD-SERVICE-ACCOUNT': getenv('POD_SERVICE_ACCOUNT'),
    }

@app.get("/")
async def root(response: Response):
    specs = {
        "players_url": "http://api.players.com/v2/players?name={name}{&size}",
        "db_url": f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}"
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
