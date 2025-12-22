from fastapi import FastAPI, Query
from datetime import datetime
from src.sensor import MetricsGenerator
from fastapi.responses import JSONResponse
import re
from typing import Optional

app = FastAPI()
generator = MetricsGenerator(min_visitors=50, max_visitors=500)

def process_dates(date: Optional[str], dates: Optional[list[str]], date_format: str, error_msg: str):
    """Helper function to process dates and validate format"""
    if not date and not dates:
        return JSONResponse(
            status_code=400,
            content={"error": "You must provide at least one 'date' or 'dates' parameter"}
        )

    dates_to_process = ([date] if date else []) + (dates if dates else [])
    
    if any(not re.match(date_format, d) for d in dates_to_process):
        return JSONResponse(
            status_code=400,
            content={"error": error_msg}
        )

    return dates_to_process
exemple_inputs = {"single_date": "2020-01-01-01-01-01",
                  "multiple_dates": ["2020-01-01-01-01-01", 
                                     "2020-01-02-01-01-01",
                                     "2020-01-03-01-01-01",
                                     "2020-01-04-01-01-01"]}

@app.get("/cities")
def get_cities_api(
    date: Optional[str] = Query(exemple_inputs["single_date"], description="Single date in YYYY-MM-DD-HH-MM-SS-MM-SS format"),
    dates: Optional[list[str]] = Query(exemple_inputs["multiple_dates"], description="Multiple dates in YYYY-MM-DD-HH-MM-SS format")
):
    """
    GET route to obtain store cities for one or multiple dates.
    Expected date format: YYYY-MM-DD-HH-MM-SS
    """
    dates_result = process_dates(
    date, 
    dates,
    r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}$',
    "Invalid date format. Use YYYY-MM-DD-HH-MM-SS format"
    )
    if isinstance(dates_result, JSONResponse):
        return dates_result
        
    try:
        date_objs = [datetime.strptime(d, "%Y-%m-%d-%H-%M-%S") for d in dates_result]
        cities = [generator.get_city(date_obj) for date_obj in date_objs]
        
        return {
            "cities": cities,
            "dates": dates_result
        }
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)})  

@app.get("/pages_viewed")
def get_pages_viewed_api(
    date: Optional[str] = Query(exemple_inputs["single_date"], description="Single date in YYYY-MM-DD-HH-MM-SS-MM-SS format"),
    dates: Optional[list[str]] = Query(exemple_inputs["multiple_dates"], description="Multiple dates in YYYY-MM-DD-HH-MM-SS format")
):
    """
    GET route to obtain number of pages viewed for one or multiple dates.
    Expected date format: YYYY-MM-DD-HH-MM-SS
    """
    dates_result = process_dates(
    date, 
    dates,
    r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}$',
    "Invalid date format. Use YYYY-MM-DD-HH-MM-SS format"
    )
    if isinstance(dates_result, JSONResponse):
        return dates_result
        
    try:
        date_objs = [datetime.strptime(d, "%Y-%m-%d-%H-%M-%S") for d in dates_result]
        pages_viewed = [generator.get_pages_viewed(date_obj) for date_obj in date_objs]
        
        return {
            "pages_viewed": pages_viewed,
            "dates": dates_result
        }
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)})  

@app.get("/visitors")
def get_visitors_api(
    date: Optional[str] = Query(exemple_inputs["single_date"], description="Single date in YYYY-MM-DD-HH-MM-SS-MM-SS format"),
    dates: Optional[list[str]] = Query(exemple_inputs["multiple_dates"], description="Multiple dates in YYYY-MM-DD-HH-MM-SS format")
):
    """
    GET route to obtain number of visitors for one or multiple dates.
    Expected date format: YYYY-MM-DD-HH-MM-SS
    """
    dates_result = process_dates(
        date, 
        dates,
        r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}$',
        "Invalid date format. Use YYYY-MM-DD-HH-MM-SS format"
    )
    if isinstance(dates_result, JSONResponse):
        return dates_result
        
    try:
        date_objs = [datetime.strptime(d, "%Y-%m-%d-%H-%M-%S") for d in dates_result]
        visitors = [generator.get_visitors(date_obj) for date_obj in date_objs]
        
        return {
            "visitors": visitors,
            "dates": dates_result
        }
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)})

@app.get("/articles/{category}")
def get_articles_by_category(
    category: str,
    date: Optional[str] = Query(exemple_inputs["single_date"], description="Single date in YYYY-MM-DD-HH-MM-SS-MM-SS format"),
    dates: Optional[list[str]] = Query(exemple_inputs["multiple_dates"], description="Multiple dates in YYYY-MM-DD-HH-MM-SS format")
):
    """
    GET route to obtain number of articles in a category for one or multiple dates.
    Expected date format: YYYY-MM-DD-HH-MM-SS-MM
    """
    if category not in generator.categories:
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid category '{category}'. Available categories: {generator.categories}"}
        )

    dates_result = process_dates(
        date, 
        dates,
        r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}$',
        "Invalid date format. Use YYYY-MM-DD-HH-MM-SS format"
    )
    if isinstance(dates_result, JSONResponse):
        return dates_result

    try:
        date_objs = [datetime.strptime(d, "%Y-%m-%d-%H-%M-%S") for d in dates_result]
        articles = [generator.get_articles_by_category(date_obj)[category] for date_obj in date_objs]
        return {
            f"{category}_articles": articles,
            "dates": dates_result
        }
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)})
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)