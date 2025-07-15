from typing import List
from job import Job

class Scraper:
    """
    A class for managing a collection of Job objects, providing methods to serialize, deserialize,
    add, remove, and update jobs.
    Attributes:
        items (List[Job]): The list of Job objects managed by the scraper.
    Methods:
        __init__(items: List[Job]):
            Initializes the Scraper with a list of Job objects.
        from_dict(d: List[dict]):
            Populates the items list from a list of dictionaries, creating Job objects for each entry.
        to_dict() -> List[dict]:
            Serializes the items list to a list of dictionaries.
        add(job: Job, ref: object):
            Adds a Job object to the items list.
        remove(job: Job, ref: object):
            Removes a Job object from the items list if it exists.
        update(job: Job, ref: object):
            Updates an existing Job in the items list by matching the URL, or adds it if not found.
    """
    def __init__(self, items: List[Job]):
        self.items = items

    def from_dict(self, d : List[dict]):
        self.items = []
        for item in d:
            job = Job(item.get('url'))
            job.id = item.get('id', Job.nextId)
            if job.id >= Job.nextId: #update nextId if id is greater
                Job.nextId = job.id + 1
            job.title = str(item.get('title'))
            job.description = str(item.get('description'))
            job.requirements = str(item.get('requirements'))
            job.contact = str(item.get('contact'))
            job.phone = str(item.get('phone'))
            job.email = str(item.get('email'))
            job.company = str(item.get('company'))
            job.location = str(item.get('location'))
            job.postedOn = str(item.get('postedOn'))
            job.hours = str(item.get('hours'))
            job.wage = str(item.get('wage'))
            job.start = str(item.get('start'))
            job.duration = str(item.get('duration'))
            job.apply = str(item.get('apply'))
            job.deadline = str(item.get('deadline'))
            job.comments = str(item.get('comments'))
            
            self.items.append(job)

    def to_dict(self) -> List[dict]:
        return [item.to_dict() for item in self.items]
    
    def add(self, job: Job, ref : object):
        self.items.append(job)

    def remove(self, job: Job, ref : object):
        if job in self.items:
            self.items.remove(job)
    
    def update(self, job: Job, ref : object):
        for i, item in enumerate(self.items):
            if item.url == job.url: #url's should be unique
                job.id = item.id
                self.items[i] = job
                return
        self.add(job, ref)  # If not found, add the job