from sqlalchemy import Column,String,Integer,Float,DateTime,ForeignKey,Date
from src.core.database import Base

class Flights(Base):
    __tablename__ = "flights_data"
    
    flight_id=Column(Integer,primary_key=True)
    source_airport=Column(String,ForeignKey("airports.airport_code"))
    destination_airport=Column(String,ForeignKey("airports.airport_code"))
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    airline_name=Column(String,nullable=False)
    flight_no = Column(String, nullable=False)
    travel_date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    stops = Column(Integer, default=0)
    flight_status = Column(String, default="Scheduled")