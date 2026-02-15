import firebase_admin
from firebase_admin import firestore
from geocoding import Geocoding
from store import Store
from scraper import ListScraper #type: ignore
import json
import asyncio

with open('creds/credentials.json', 'r') as file:
        data = json.load(file)
        PROJECT_ID = data.get('project_id')
        COLL_NAME = data.get('coll_name')
        GEOCODE_API_KEY = data.get('geocode_api_key')

app = firebase_admin.initialize_app(options={'projectId': PROJECT_ID})
db = firestore.client()

geocode = Geocoding(GEOCODE_API_KEY)

doc_ref = db.collection(COLL_NAME)

store = Store(doc_ref)

scraper = ListScraper()

async def main():
    await scraper.scrape(store, geocode)

asyncio.run(main())