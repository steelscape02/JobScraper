from typing import Optional
from job import Job
from firebase_admin.firestore import firestore

class Store:
    fireDB : firestore.CollectionReference
    def __init__(self, db : Optional[firestore.CollectionReference] = None):
        if db is not None:
            self.fireDB = db
        pass
    

    def remove(self, url: str):
        ext = url.split("/")[-1]  # Get the last part of the URL
        self.fireDB.document(ext).delete()
    
    def update(self, job: Job):
        self.fireDB.document(job.id).set(job.to_dict())

    def Display(self):
        docs = self.fireDB.stream()
        for doc in docs:
            print(f"{doc.id} => {doc.to_dict()}")