import firebase_admin
from firebase_admin import firestore
from scraper import Job #type: ignore

# Application Default credentials are automatically created.

PROJECT_ID = "job-scraper-5a9d0"  # Replace with your actual project ID
app = firebase_admin.initialize_app(options={'projectId': PROJECT_ID})
db = firestore.client()

thing = Job("https:\\\\example.com\\job1")
col = db.collection("jobs_list")

col.document(thing.url).set(thing.to_dict())