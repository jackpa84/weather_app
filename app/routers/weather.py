from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.services import WeatherService

router = APIRouter()
weather_service = WeatherService()

@router.get('/weather')
async def clima(request: Request):
    city = request.query_params.get('city')
    if not city:
        raise HTTPException(status_code=400, detail="Not found query parameter 'city'")
    weather_data = weather_service.get_weather(city)
    if weather_data.get("cod") != 200:
        raise HTTPException(status_code=404, detail="City not found")
    weather_description = weather_data['weather'][0]['description']
    funny_text = weather_service.generate_funny_text(city, weather_description)
    translated_text = weather_service.translate_to_portuguese(funny_text)
    return JSONResponse(content={"message": translated_text})