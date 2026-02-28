from sqlalchemy.orm import Session
from src.models.flight import Flights
from src.models.search_history import SearchHistory
# Duration in minutes
def calculate_duration_minutes(flight):
    duration = flight.arrival_time - flight.departure_time
    return int(duration.total_seconds() / 60)

def format_duration(flight):
    minutes = calculate_duration_minutes(flight)

    hours = minutes // 60
    mins = minutes % 60
    if hours == 0:
        return f"{mins}m"
    if mins == 0:
        return f"{hours}h"
    return f"{hours}h {mins:02d}m"

def calculate_best_score(flight):
    duration = calculate_duration_minutes(flight)

    score = (
        flight.price * 0.5 +
        duration * 0.3 +
        flight.stops * 200
    )
    return score

def search_flights(db: Session, search_data,current_user):
    history = SearchHistory(
        user_id=current_user.user_id,
        source=search_data.source,
        destinations=",".join(search_data.destinations),
        start_date=search_data.start_date,
        end_date=search_data.end_date,
        budget=search_data.budget,
    )
    db.add(history)
    db.commit()
    
    query = db.query(Flights).filter(
        Flights.source_airport == search_data.source,
        Flights.destination_airport.in_(search_data.destinations),
        Flights.travel_date.between(
            search_data.start_date,
            search_data.end_date
        )
    )
    if search_data.budget is not None:

        budget_query = query.filter(
            Flights.price <= search_data.budget
        ).order_by(Flights.price.asc())

        results = budget_query.all()

        if not results:
            results = query.order_by(Flights.price.asc()).all()
            message = "No flights under budget. Showing cheapest available."
        else:
            message = "Flights under budget"

    else:
        results = query.order_by(Flights.price.asc()).all()
        message = "Suggested cheapest flights"

    if not results:
        return {
            "message": "No flights found",
            "flights": []
        }
    cheapest_flight = min(results, key=lambda x: x.price)

    fastest_flight = min(
        results,
        key=lambda x: calculate_duration_minutes(x)
    )

    best_flight = min(
        results,
        key=lambda x: calculate_best_score(x)
    )
    return {
        "message": message,

        "summary": {
            "cheapest": {
                "price": cheapest_flight.price,
                "duration": format_duration(cheapest_flight)
            },
            "fastest": {
                "price": fastest_flight.price,
                "duration": format_duration(fastest_flight)
            },
            "best": {
                "price": best_flight.price,
                "duration": format_duration(best_flight)
            }
        },

        "flights": results
    }