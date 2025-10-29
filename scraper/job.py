class Job:
    id = ""
    title = ""
    description = ""
    requirements = ""
    contact : str | None = ""
    phone = ""
    email = ""
    company : str | None = ""
    location = ""
    postedOn = ""
    postedOnRaw = 0
    hours = ""
    wage = ""
    start = ""
    duration = ""
    apply = ""
    deadline = ""
    comments = ""

    def __init__(self, url):
        self.url = url

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
            'postedOnRaw' : self.postedOnRaw,
            'hours' : self.hours,
            'wage' : self.wage,
            'start' : self.start,
            'duration' : self.duration,
            'apply' : self.apply,
            'deadline' : self.deadline,
            'comments' : self.comments
        } 
    
    def from_dict(self, d: dict):
        self.id = str(d.get('id', ""))
        self.title = str(d.get('title', ""))
        self.description = str(d.get('description', ""))
        self.requirements = str(d.get('requirements', ""))
        self.contact = str(d.get('contact', ""))
        self.phone = str(d.get('phone', ""))
        self.email = str(d.get('email', ""))
        self.company = str(d.get('company', ""))
        self.location = str(d.get('location', ""))
        self.postedOn = str(d.get('postedOn', ""))
        self.postedOnRaw = int(d.get('postedOnRaw', 0))
        self.hours = str(d.get('hours', ""))
        self.wage = str(d.get('wage', ""))
        self.start = str(d.get('start', ""))
        self.duration = str(d.get('duration', ""))
        self.apply = str(d.get('apply', ""))
        self.deadline = str(d.get('deadline', ""))
        self.comments = str(d.get('comments', ""))
        # Ensure the URL is always a string
        self.url = str(d.get('url', self.url))