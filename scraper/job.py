class Job:
    nextId = 0 # Static variable to keep track of the next job ID

    title = ""
    description = ""
    requirements = ""
    contact = ""
    phone = ""
    email = ""
    company = ""
    location = ""
    postedOn = ""
    hours = ""
    wage = ""
    start = ""
    duration = ""
    apply = ""
    deadline = ""
    comments = ""

    def __init__(self, url):
        self.url = url
        self.id = Job.nextId
        Job.nextId += 1

    def to_dict(self):
        return {
            'id' : self.id,
            'url' : self.url,
            'title' : self.title,
            'description' : self.description,
            'requirements' : self.requirements,
            'contact' : self.contact,
            'phone' : self.phone,
            'email' : self.email,
            'company' : self.company,
            'location' : self.location,
            'postedOn' : self.postedOn,
            'hours' : self.hours,
            'wage' : self.wage,
            'start' : self.start,
            'duration' : self.duration,
            'apply' : self.apply,
            'deadline' : self.deadline,
            'comments' : self.comments
        } 