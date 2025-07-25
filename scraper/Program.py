import firebase_admin
from firebase_admin import firestore
from scraper import Scraper #type: ignore
from job import Job
import json

with open('creds/credentials.json', 'r') as file:
        data = json.load(file)
        PROJECT_ID = data.get('project_id')
        COLL_NAME = data.get('coll_name')

app = firebase_admin.initialize_app(options={'projectId': PROJECT_ID})
db = firestore.client()

doc_ref = db.collection(COLL_NAME)

scraper = Scraper(doc_ref)
testJob = Job("https://example.com/job1")
scraper.update(testJob)

scraper.Display()
