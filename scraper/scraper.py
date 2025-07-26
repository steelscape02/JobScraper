import requests
from bs4 import BeautifulSoup
import re
from job import Job 
from store import Store

class ListScraper:
    store = []
    BASE_URL = "https://www.byui.edu/help-wanted-postings"

    @staticmethod
    async def scrape(store: Store):
        ListScraper.store.clear()
        await ListScraper.ScrapeAllJobs(store, ListScraper.BASE_URL)

    @staticmethod
    async def ScrapeAllJobs(store, base_url, ext=""):
        try:
            full_url = base_url + ext
            response = requests.get(full_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')

            links = soup.find_all('a')

            for link in links:
                href = link.get('href')
                text = link.text.strip() # Use .text for text content

                if "Get Involved" in text:
                    if (href != None) : await ListScraper.ScrapeJob(store, href)
                
                elif "Next" in text: 
                    if (href != None) : await ListScraper.ScrapeAllJobs(store, base_url,href)
                

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    async def ScrapeJob(store, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            job = Job(url)
            job.id = url.split("/")[-1]  # Use the last part of the URL as the job ID

            # Posted Date
            # C#: document.GetElementsByClassName("ArticlePage-datePublished")[0].TextContent;
            posted_date_element = soup.find(class_="ArticlePage-datePublished")
            if posted_date_element:
                job.postedOn = posted_date_element.text.strip()
            # Headers containing job details
            # C#: document.GetElementsByClassName("RichTextArticleBody");
            headers = soup.find_all(class_="RichTextArticleBody")

            for header in headers:
                header_text = header.text

                # Extracting details using regex (translated from C# regexes)
                job.title = ListScraper._extract_title(header_text)
                if job.title == "Job Title Name": # Check for placeholder
                    continue

                job.description = ListScraper._extract_description(header_text)
                job.requirements = ListScraper._extract_requirements(header_text)
                if not job.requirements:
                    job.requirements = ListScraper._extract_requirements_advanced(header_text)

                job.contact = ListScraper._extract_contact_name(header_text)
                job.phone = ListScraper._extract_phone(header_text)
                job.email = ListScraper._extract_email(header_text)
                job.company = ListScraper._extract_company_name(header_text)
                job.location = ListScraper._extract_address(header_text)
                if not job.location:
                    job.location = ListScraper._extract_address_advanced(header_text)

                job.hours = ListScraper._extract_hours(header_text)
                job.wage = ListScraper._extract_wage(header_text)
                if not job.wage:
                    job.wage = ListScraper._extract_wage_advanced(header_text)

                job.start = ListScraper._extract_start(header_text)
                job.duration = ListScraper._extract_duration(header_text)
                if not job.duration:
                    job.duration = ListScraper._extract_duration_advanced(header_text)

                job.apply = ListScraper._extract_apply(header_text)
                job.deadline = ListScraper._extract_deadline(header_text)
                job.comments = ListScraper._extract_comments(header_text)
                if not job.comments:
                    job.comments = ListScraper._extract_comments_advanced(header_text)

                store.update(job)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching job URL {url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while scraping job {url}: {e}")

    # --- Regex Extraction Methods (Python equivalent) ---
    @staticmethod
    def _extract_contact_name(input_string):
        # Original: r"(?<=Contact Name\s*)([\s\S]*?)(?=\s*Company)"
        # Problem: \s* in look-behind
        # Solution: Match "Contact Name" and the spaces, then capture the actual value.
        regex = r"Contact Name\s*([\s\S]*?)\s*Company" # Changed to match the prefix, capture content, then match the suffix
        match = re.search(regex, input_string)
        # We now need to access group(1) because group(0) is the entire match including "Contact Name" and "Company"
        return match.group(1).strip() if match else None

    @staticmethod
    def _extract_company_name(input_string):
        regex = r"Company\s*([\s\S]*?)\s*Contact Phone Number"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else None

    @staticmethod
    def _extract_phone(input_string):
        regex = r"Contact Phone Number\s*([\s\S]*?)\s*Address"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_address(input_string):
        # Original: r"(?<=Address\s*)(.*)(?=\s*Email Address)"
        # The C# AddressRegex was: "(?<=Address\s*)(.*)(?=\s*Email Address)"
        # This one is a bit tricky if "Email Address" is not always there immediately after the address.
        # Let's consider the full content between markers.
        regex = r"Address\s*(.*?)\s*Email Address" # Capture non-greedy everything after "Address" and before "Email Address"
        match = re.search(regex, input_string)
        if match:
            value = match.group(1).strip()
            # If the C# logic was specifically to remove ", City, State" from the *matched value*,
            # you'd do it here:
            # value = value.replace(", City, State", "") # Or more robustly with regex.
            return value
        return ""


    @staticmethod
    def _extract_address_advanced(input_string):
        regex = r"Address, City, State\s*(.*?)\s*Email Address"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_email(input_string):
        regex = r"Email Address\s*([\s\S]*?)\s*Job Title"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_title(input_string):
        regex = r"Job Title\s*([\s\S]*?)\s*Job Description"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_description(input_string):
        regex = r"Job Description\s*([\s\S]*?)\s*Requirements"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_requirements(input_string):
        regex = r"Requirements/Qualifications\s*(.*?)\s*Start Date"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_requirements_advanced(input_string):
        regex = r"Requirements / Qualifications\s*(.*?)\s*Start Date"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_start(input_string):
        regex = r"Start Date\s*([\s\S]*?)\s*Duration"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_duration(input_string):
        regex = r"Duration/End Date\s*([\s\S]*?)\s*Hours"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_duration_advanced(input_string):
        regex = r"Duration / End Date\s*([\s\S]*?)\s*Hours"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_hours(input_string):
        regex = r"Hours\s*([\s\S]*?)\s*Pay"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_wage(input_string):
        regex = r"Pay/Wage\s*([\s\S]*?)\s*How to Apply"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_wage_advanced(input_string):
        regex = r"Pay / Wage\s*([\s\S]*?)\s*How to Apply"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_apply(input_string):
        regex = r"How to Apply\s*([\s\S]*?)\s*Application Deadline"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_deadline(input_string):
        regex = r"Application Deadline:\s*([\s\S]*?)\s*Other Questions"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_comments(input_string):
        # This one ends with $, so it's slightly different.
        regex = r"Other Questions/Comments:\s*([\s\S]*)$"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_comments_advanced(input_string):
        # This one ends with $, so it's slightly different.
        regex = r"Other Questions / Comments:\s*([\s\S]*)$"
        match = re.search(regex, input_string)
        return match.group(1).strip() if match else ""