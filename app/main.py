# app/main.py

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import utm
from fastapi.templating import Jinja2Templates
from app.olc import encode


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Template directory setup for rendering HTML
templates = Jinja2Templates(directory="templates")


def get_utm_latitude_letter(latitude: float) -> str:
    """
    Given a latitude in decimal degrees, return the corresponding UTM latitude band letter.
    
    The latitude bands range from -80 to +84 degrees, each band is 8 degrees wide.
    
    :param latitude: Latitude in decimal degrees
    :return: UTM latitude band letter
    """
    if latitude < -80 or latitude > 84:
        raise ValueError("Latitude out of UTM bounds. Must be between -80 and 84 degrees.")

    # Define the letters for the UTM latitude bands (C to X, skipping I and O)
    latitude_bands = "CDEFGHJKLMNPQRSTUVWX"
    
    # The UTM bands start at -80 degrees, each spanning 8 degrees
    band_index = int((latitude + 80) // 8)

    return latitude_bands[band_index]

# Helper function to convert decimal degrees to UTM
def decimal_degrees_to_utm(lat, lon):
    """
    Convert latitude and longitude from decimal degrees to UTM coordinates.
    """
    # Get the UTM zone and zone letter
    utm_x, utm_y, utm_zone, utm_zone_letter = utm.from_latlon(lat, lon)

    return utm_x, utm_y, utm_zone, utm_zone_letter


# HTML page to show form for latitude and longitude input
@app.get("/", response_class=HTMLResponse)
async def get_location_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Endpoint to handle the form and display the location in decimal and UTM
@app.post("/coordinates/", response_class=HTMLResponse)
async def show_coordinates(request: Request, latitude: float = Form(...), longitude: float = Form(...)):
    # Get UTM coordinates
    utm_x, utm_y, utm_zone, utm_zone_letter = decimal_degrees_to_utm(latitude, longitude)
    openloccode = encode(latitude, longitude, 11)
    
    print(f"Latitude: {latitude}, Longitude: {longitude}")
    # Return the results in the response
    return templates.TemplateResponse("result.html", {
        "request": request,
        "latitude": latitude,
        "longitude": longitude,
        "utm_x": int(utm_x),
        "utm_y": int(utm_y),
        "utm_zone": utm_zone,
        "utm_zone_letter": utm_zone_letter,
        "openlocationcode": openloccode
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)