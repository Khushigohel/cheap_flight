from pydantic import BaseModel
from typing import List,Optional
from datetime import date

class FlightSearchRequest(BaseModel):
    source:str
    destinations:List[str]
    start_date:date
    end_date:date
    budget:Optional[float]=None
    sort_by: Optional[str] = "cheapest"