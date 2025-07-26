from typing import Optional
from job import Job
from firebase_admin.firestore import firestore

class Store:
    fireDB : firestore.CollectionReference
    def __init__(self, db : Optional[firestore.CollectionReference] = None):
        if db is not None:
            self.fireDB = db
        pass
    
    # def add(self, job: Job):
    #     url = job.url.replace("/", "\\")  # Normalize URL format
    #     self.fireDB.document(url).set(job.to_dict())

    def remove(self, url: str):
        format_url = url.replace("/", "\\")
        self.fireDB.document(format_url).delete()
    
    def update(self, job: Job):
        url = job.url.replace("/", "\\")  # Normalize URL format
        self.fireDB.document(url).set(job.to_dict())

    def Display(self):
        docs = self.fireDB.stream()
        for doc in docs:
            print(f"{doc.id} => {doc.to_dict()}")