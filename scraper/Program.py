import firebase_admin
from firebase_admin import firestore
from store import Store
from scraper import ListScraper #type: ignore
import json
import asyncio

with open('creds/credentials.json', 'r') as file:
        data = json.load(file)
        PROJECT_ID = data.get('project_id')
        COLL_NAME = data.get('coll_name')

app = firebase_admin.initialize_app(options={'projectId': PROJECT_ID})
db = firestore.client()

doc_ref = db.collection(COLL_NAME)

store = Store(doc_ref)

scraper = ListScraper()

async def main():
    await scraper.scrape(store)

asyncio.run(main())