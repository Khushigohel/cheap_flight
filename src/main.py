from fastapi import FastAPI
from src.core.database import Base, engine
from src.routes import user_routes
from src.routes import google_auth_routes
from src.models.airport import Airport
from src.models.flight import Flights
from src.routes import flight_search_routes

app = FastAPI(title="User Fast Api")
Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
app.include_router(google_auth_routes.router)
app.include_router(flight_search_routes.router)
