import requests
import time
from datetime import datetime, timedelta

from src.core.database import SessionLocal
from src.models.flight import Flights
from src.models.airport import Airport
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("SERP_API_KEY")
url = "https://serpapi.com/search"

MAX_API_CALLS = 30   # Only 3 API calls for testing

start_date = datetime.today().date()
end_date = start_date + timedelta(days=4)

def get_all_airport_codes(db):
    airports = db.query(Airport).all()
    return [a.airport_code for a in airports]


def fetch_multi_day_flights():
    db = SessionLocal()
    total_inserted = 0 
    api_calls = 0   # testing

    all_airports = get_all_airport_codes(db)[:3]
    
    current_date = start_date

    while current_date <= end_date:
        outbound_date = current_date.strftime("%Y-%m-%d")
        for source_code in all_airports:
            for dest_code in all_airports:
                
                if source_code == dest_code:
                    continue
                # testing
                if api_calls >= MAX_API_CALLS:
                    print("\n⚠ API test limit reached. Stopping safely.")
                    db.close()
                    return
                
                print(f"Fetching {source_code} → {dest_code} on {outbound_date}")
                params = {
                    "engine": "google_flights",
                    "departure_id": source_code,
                    "arrival_id": dest_code,
                    "outbound_date": outbound_date,
                    "currency": "INR",
                    "gl": "in",
                    "api_key": API_KEY,
                    "type": "2",
                }
                response = requests.get(url, params=params)
                api_calls += 1
                print(f"API Call Count: {api_calls}")
                data = response.json()

                if "error" in data:
                    print("API Error:", data["error"])
                    continue
                flights = data.get("best_flights", []) + data.get("other_flights", [])

                for f in flights:
                    leg = f.get("flights", [{}])[0]

                    departure_time_str = leg.get("departure_airport", {}).get("time")
                    arrival_time_str = leg.get("arrival_airport", {}).get("time")

                    try:
                        departure_time = datetime.fromisoformat(departure_time_str)
                        arrival_time = datetime.fromisoformat(arrival_time_str)
                    except:
                        continue

                    flight = Flights(
                        source_airport=source_code,
                        destination_airport=dest_code,
                        departure_time=departure_time,
                        arrival_time=arrival_time,
                        airline_name=leg.get("airline"),
                        flight_no=leg.get("flight_number", "N/A"),
                        travel_date=current_date,
                        price=f.get("price", 0),
                        currency="INR",
                        stops = len(f.get("flights", [])) - 1,
                        flight_status = f.get("status", "Scheduled")
                    )

                    db.add(flight) 
                    total_inserted += 1
                   
                db.commit()
                time.sleep(1)
        current_date += timedelta(days=1)

    db.close()
    print(f"Inserted {total_inserted} flights successfully")
    print(f" Total API Calls Used: {api_calls}")


if __name__ == "__main__":
    fetch_multi_day_flights()
