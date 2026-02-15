
import time
import requests


class Geocoding:
    def __init__(self, api_key):
        self.api_key = api_key

    def geocode(self, address, max_retries: int = 5) -> tuple[float, float] | None:
        url = f"https://geocode.maps.co/search?q={address}&countrycodes=us&api_key={self.api_key}" #forward lookup

        if max_retries <= 0:
            raise ValueError(f"Max retries exceeded for geocoding address: {address}")
            return None
        try:
            response = requests.get(url)
            response.raise_for_status()
            if(response.status_code == 429):
                retry_after = int(response.headers.get("Retry-After", 1))
                if(retry_after > 0):
                    #Rate limit exceeded. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                else:
                    time.sleep(1);
                return self.geocode(address, max_retries - 1)
                    
            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return (lat, lon)
        except Exception:
            return None