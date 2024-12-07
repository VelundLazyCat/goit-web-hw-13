from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
import my_routes
import auth_routes
import users_routes
from my_db import get_db
from models import Contact
import redis.asyncio as redis
from config import settings
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix='/api')
app.include_router(my_routes.router, prefix='/api')
app.include_router(users_routes.router, prefix='/api')


@app.get('/')
def index():
    return {'message': 'Welcome to Web Assistant'}


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/api/healthchecker")
async def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(select(Contact)).all()

        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="Error connecting to the database")
