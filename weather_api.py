import urllib.parse
import requests


# --- Geocoding: turn user text into (lat, lon, human_readable_name) -----------------
def geocode_location(location: str):
    """
    Convert a U.S. city/ZIP string into (latitude, longitude, display_name),
    trying the Census Geocoder first, then Nominatim (OpenStreetMap).
    """
    print(f"🔍 Looking up coordinates for: {location}")

    # 1) Try Census Geocoding API
    try:
        base_url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
        params = {
            "address": location,
            "benchmark": "Public_AR_Current",
            "format": "json",
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            matches = data.get("result", {}).get("addressMatches", [])
            if matches:
                match = matches[0]
                lat = match["coordinates"]["y"]
                lon = match["coordinates"]["x"]
                matched_address = match["matchedAddress"]
                print(f"✅ Found: {matched_address}")
                print(f"📍 Coordinates: {lat}, {lon}")
                return lat, lon, matched_address
    except Exception:
        print("⚠️  Census API failed, trying backup method...")

    # 2) Fallback: Nominatim (OpenStreetMap), zip gets “, United States” added
    try:
        if location.strip().isdigit() and len(location.strip()) == 5:
            search_query = f"{location}, United States"
        else:
            search_query = location

        nominatim_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": search_query,
            "format": "json",
            "limit": 1,
            "countrycodes": "us",
        }
        headers = {"User-Agent": "WeatherApp/1.0 (Python Weather Forecast Tool)"}

        url = f"{nominatim_url}?{urllib.parse.urlencode(params)}"
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data:
                result = data[0]
                lat = float(result["lat"])
                lon = float(result["lon"])
                display_name = result["display_name"]
                print(f"✅ Found: {display_name}")
                print(f"📍 Coordinates: {lat}, {lon}")
                return lat, lon, display_name
    except Exception as e:
        print(f"❌ Backup geocoding failed: {e}")

    # If both methods fail
    print("❌ Location not found. Try a different format.")
    print("   Examples: 'Appleton, WI' or '54911' or 'Oshkosh, Wisconsin'")
    return None


# --- Forecast retrieval: call api.weather.gov for a given point ----------
def get_weather_forecast(latitude: float, longitude: float):
    """
    Fetch NWS forecast periods for given coordinates.
    Returns a list of periods or None on error.
    """
    try:
        points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
        headers = {"User-Agent": "WeatherApp/1.0 (your.email@example.com)"}

        # Get metadata including forecast URL
        response = requests.get(points_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Unable to fetch location data (status {response.status_code})")
            print("Note: NWS API only covers the United States.")
            return None

        data = response.json()
        forecast_url = data["properties"]["forecast"]

        # Get the actual forecast periods
        forecast_response = requests.get(forecast_url, headers=headers, timeout=10)
        if forecast_response.status_code != 200:
            print(f"❌ Unable to fetch forecast (status {forecast_response.status_code})")
            return None

        forecast_data = forecast_response.json()
        return forecast_data["properties"]["periods"]

    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out. Check your internet connection.")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Unable to connect to weather service. Check your internet.")
    except KeyError as e:
        print(f"❌ Error: Unexpected response format from API. Missing key: {e}")
    except Exception as e:
        print(f"❌ Error: An unexpected error occurred: {e}")

    return None


# --- CLI presentation: print forecast nicely to the console -------------
def display_forecast(periods):
    """Print a 7‑day (14 period) forecast to the console."""
    if not periods:
        print("\n❌ No forecast data available.")
        return

    print("\n" + "=" * 50)
    print("7-DAY WEATHER FORECAST")
    print("=" * 50 + "\n")

    for period in periods[:14]:
        print(f"📅 {period['name']}:")
        print(f"   🌡️  Temperature: {period['temperature']}°{period['temperatureUnit']}")
        print(f"   ☁️  Conditions: {period['shortForecast']}")
        print(f"   💨 Wind: {period['windSpeed']} {period['windDirection']}")
        print()


# --- CLI flow: prompt user, geocode, fetch, display, optional retry -----
def main():
    """Command-line flow for the NWS Weather Forecast App."""
    print("=" * 50)
    print("Welcome to the NWS Weather Forecast App!")
    print("=" * 50)
    print("\nEnter a U.S. location or zip code")
    print("Examples: 'Appleton, WI' or '54911' or 'Chicago, IL'\n")

    latitude = longitude = None

    while True:
        location = input("Enter location: ").strip()
        if not location:
            print("❌ Please enter a location.\n")
            continue

        coords = geocode_location(location)
        if coords:
            latitude, longitude, _ = coords
            break
        else:
            print("\nTry again with a different format.\n")

    if latitude is None or longitude is None:
        return # could also be sys.exit(1)

    print("\n📡 Fetching weather forecast...\n")
    periods = get_weather_forecast(latitude, longitude)
    display_forecast(periods)

    print("\n" + "=" * 50)
    retry = input("Check another location? (y/n): ").strip().lower()
    if retry == "y":
        print()
        main()
    else:
        print("\nThanks for using the Weather App! Stay safe out there. 🌤️")


if __name__ == "__main__":
    main()