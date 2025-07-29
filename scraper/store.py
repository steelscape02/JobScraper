from typing import Optional
from job import Job
from firebase_admin.firestore import firestore

class Store:
    fireDB : firestore.CollectionReference
    def __init__(self, db : Optional[firestore.CollectionReference] = None):
        if db is not None:
            self.fireDB = db

    def remove(self, job: Job):
        self.fireDB.document(job.id).delete()
    
    def update(self, job: Job):
        self.fireDB.document(job.id).set(job.to_dict())

    def has(self, job : Job) -> bool:
        return self.fireDB.document(job.id).get().exists
    
    def Display(self): #dev only
        docs = self.fireDB.stream()
        for doc in docs:
            print(f"{doc.id} => {doc.to_dict()}")