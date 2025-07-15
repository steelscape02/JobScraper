import firebase_admin
from firebase_admin import credentials, firestore
from scraper.scraper import Scraper
from scraper.job import Job

#tool to store stuff: Firebase
#tool to launch this funky thing: Google Cloud Run wit a Cloud Scheduler job
JOBS_STORE = "jobs_store"

with open("creds/credentials.json", "r") as f:
    creds = f.read()
    creds = eval(creds)  # Convert string to dictionary
    creds = creds.get("firestore_creds", "")

#TODO: Create a new svc account for this tied to this firestore db
#INFO: Sync has been completed with cloud stuff. Finish this file and imp firestore in job and scraper (as needed)

cred = credentials.Certificate(creds)
app = firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection(JOBS_STORE).document("jobs")

# doc = doc_ref.get()
# inv = Scraper([])
# if any(doc):
#     inv.from_dict(d=doc)