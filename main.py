from fastapi import Depends, FastAPI, Query
from fastapi.security.api_key import APIKey
from datetime import datetime
from src.sensor import MetricsGenerator
from src.utilities import process_dates
from src.variables import EXAMPLE_INPUTS
from src.utilities import get_api_key
from fastapi.responses import JSONResponse
from typing import Optional




app = FastAPI()
generator = MetricsGenerator(min_visitors=50, max_visitors=500)


@app.get("/cities")
def get_cities_api(
    date: Optional[str] = Query(EXAMPLE_INPUTS["single_date"], description="Single date in YYYY-MM-DD-HH-MM-SS-MM-SS format"),
    dates: Optional[list[str]] = Query(EXAMPLE_INPUTS["multiple_dates"], description="Multiple dates in YYYY-MM-DD-HH-MM-SS format"),
    api_key_header: APIKey = Depends(get_api_key)
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
    date: Optional[str] = Query(EXAMPLE_INPUTS["single_date"], description="Single date in YYYY-MM-DD-HH-MM-SS-MM-SS format"),
    dates: Optional[list[str]] = Query(EXAMPLE_INPUTS["multiple_dates"], description="Multiple dates in YYYY-MM-DD-HH-MM-SS format"),
    api_key_header: APIKey = Depends(get_api_key)

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
    date: Optional[str] = Query(EXAMPLE_INPUTS["single_date"], description="Single date in YYYY-MM-DD-HH-MM-SS-MM-SS format"),
    dates: Optional[list[str]] = Query(EXAMPLE_INPUTS["multiple_dates"], description="Multiple dates in YYYY-MM-DD-HH-MM-SS format"),
    api_key_header: APIKey = Depends(get_api_key)

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
    date: Optional[str] = Query(EXAMPLE_INPUTS["single_date"], description="Single date in YYYY-MM-DD-HH-MM-SS-MM-SS format"),
    dates: Optional[list[str]] = Query(EXAMPLE_INPUTS["multiple_dates"], description="Multiple dates in YYYY-MM-DD-HH-MM-SS format"),
    api_key_header: APIKey = Depends(get_api_key)
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