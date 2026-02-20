from fastapi import FastAPI
from src.core.database import Base, engine
from src.routes import user_routes

app = FastAPI(title="User Fast Api")
Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)