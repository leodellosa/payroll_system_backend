from fastapi import FastAPI
from app.api.v1 import api_router
from .db.session import create_db_and_tables
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

def lifespan(app: FastAPI):
    create_db_and_tables()
    print("Database and tables created.")
    yield

app = FastAPI(title="My FastAPI App", lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
