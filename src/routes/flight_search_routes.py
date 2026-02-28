from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.flight_schema import FlightSearchRequest
from src.crud.flights_search import search_flights
from src.core.database import get_db
from src.utils.auth import get_current_user

router = APIRouter()

@router.post("/search-flights")
def search_flights_api(search_data: FlightSearchRequest,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return search_flights(db, search_data,current_user)