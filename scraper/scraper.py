import requests
from bs4 import BeautifulSoup
import re
from job import Job 
from store import Store
from geocoding import Geocoding
from datetime import datetime, timezone

class ListScraper:
    local = []
    BASE_URL = "https://www.byui.edu/help-wanted-postings"

    @staticmethod
    async def scrape(store: Store, geocoder: Geocoding):
        await ListScraper.ScrapeAllJobs(store, geocoder, ListScraper.BASE_URL)

    @staticmethod
    async def ScrapeAllJobs(store : Store, geocoder: Geocoding, base_url : str, ext : str =""):
        
        try:
            full_url = base_url + ext
            response = requests.get(full_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')

            links = soup.find_all('a')

            for link in links:
                href = link.get('href')
                text = link.text.strip()
                if "Get Involved" in text:
                    if (href != None) : 
                        ListScraper.local.append(await ListScraper.ScrapeJob(store, geocoder, href))
                
                elif "Next" in text: 
                    if (href != None): 
                        await ListScraper.ScrapeAllJobs(store, geocoder, base_url,href)
                        return
            for job in store.fireDB.stream():
                if job is not None and job.id not in ListScraper.local:
                    store.remove(job.id)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    async def ScrapeJob(store, geocoder, url) -> Job | None:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            job = Job(url)
            job.id = url.split("/")[-1]  # Use the last part of the URL as the job ID

            posted_date_element = soup.find(class_="ArticlePage-datePublished")
            if posted_date_element:
                date = posted_date_element.text.strip()
                #check that date exists
                job.postedOn = date if len(date) > 0 else "N/A"
                try:
                    dt = datetime.strptime(date, "%B %d, %Y").replace(tzinfo=timezone.utc)
                    job.postedOnRaw = int(dt.timestamp())
                except ValueError:
                    job.postedOnRaw = 0

            headers = soup.find_all(class_="RichTextArticleBody")

            for header in headers:
                header_text = header.text

                job.title = ListScraper._extract_title(header_text)
                if job.title == "Job Title Name":
                    continue
                job.description = ListScraper._extract_description(header_text)
                job.requirements = ListScraper._extract_requirements(header_text)
                job.contact = ListScraper._extract_contact_name(header_text)
                job.phone = ListScraper._extract_phone(header_text)
                job.email = ListScraper._extract_email(header_text)
                job.company = ListScraper._extract_company_name(header_text)
                job.location = ListScraper._extract_address(header_text)
                geocoded = geocoder.geocode(job.location)
                if geocoded:
                    job.latitude, job.longitude = geocoded

                job.hours = ListScraper._extract_hours(header_text)

                job.wage = ListScraper._extract_wage(header_text)
                x = re.findall(r'[\d,\.]+(?<=\d)', job.wage.strip())

                try:
                    x = [item.replace(',', '') for item in x]
                    wages = [float(item) for item in x]
                    
                    if "email" in job.wage.lower():
                        job.wageRaw = 0.0
                    elif "call" in job.wage.lower():
                        job.wageRaw = 0.0
                    elif "text" in job.wage.lower():
                        job.wageRaw = 0.0
                    elif len(wages) >= 1:
                        job.wageRaw = sum(wages) / len(wages)
                    else:
                        job.wageRaw = float(x[0]) if x else 0.0
                except ValueError:
                    job.wageRaw = 0.0

                job.start = ListScraper._extract_start(header_text)
                job.duration = ListScraper._extract_duration(header_text)
                job.apply = ListScraper._extract_apply(header_text)
                job.deadline = ListScraper._extract_deadline(header_text)
                job.comments = ListScraper._extract_comments(header_text)

                store.update(job)
                return job.id

        except requests.exceptions.RequestException as e:
            print(f"Error fetching job URL {url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while scraping job {url}: {e}")

    @staticmethod
    def _extract_contact_name(input_string):
        regex = r"Contact Name(.*?)(?=Company)"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else None

    @staticmethod
    def _extract_company_name(input_string):
        regex = r"Company(.*?)(?=(Contact|Address))"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else None

    @staticmethod
    def _extract_phone(input_string):
        regex = r"Contact Phone Number(.*?)(?=Address)"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_address(input_string):
        regex = r"(Address|State)(.*?)(?=Email Address)"
        match = re.search(regex, input_string)
        return match.group(2).strip() if match else ""

    @staticmethod
    def _extract_email(input_string):
        regex = r"Email Address(.*?)(?=Job Title)"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_title(input_string):
        regex = r"Job Title(.*?)(?=Job Description)"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_description(input_string):
        regex = r"Job Description(.*?)(?=Requirements)"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_requirements(input_string):
        regex = r"Requirements(/|\s/\s)Qualifications(.*?)(?=Start Date)"
        match = re.search(regex, input_string)
        return match.group(2).strip() if match else ""
    
    @staticmethod
    def _extract_start(input_string):
        regex = r"Start Date(.*?)(?=Duration)"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_duration(input_string):
        regex = r"Duration(/|\s/\s)End Date(.*?)(?=Hours)"
        match = re.search(regex, input_string)
        return match.group(2).strip() if match else ""

    @staticmethod
    def _extract_hours(input_string):
        regex = r"Hours(.*?)(?=Pay)"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_wage(input_string):
        regex = r"Pay(/|\s/\s)Wage(.*?)(?=How to Apply)"
        match = re.search(regex, input_string)
        return match.group(2).strip() if match else ""

    @staticmethod
    def _extract_apply(input_string):
        regex = r"How to Apply:(.*?)(?=Application Deadline)"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_deadline(input_string):
        regex = r"Application Deadline:(.*?)(?=Other Questions)"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_comments(input_string):
        regex = r"Other Questions(/|\s/\s)Comments:(.*?)(?=$)"
        match = re.search(regex, input_string)
        return match.group(2).strip() if match else ""