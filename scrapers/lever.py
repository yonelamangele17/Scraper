import requests

from config.companies import (
    LEVER_COMPANIES,
    KEYWORDS,
    LOCATIONS,
)

from utils.job import Job


def scrape():

    jobs = []

    for company in LEVER_COMPANIES:

        url = f"https://api.lever.co/v0/postings/{company}?mode=json"

        try:

            response = requests.get(url, timeout=15)

            if response.status_code != 200:
                continue

            postings = response.json()

            for job in postings:

                title = job.get("text", "")
                location = job.get("categories", {}).get("location", "")

                if not any(word in title.lower() for word in KEYWORDS):
                    continue

                if not any(place in location.lower() for place in LOCATIONS):
                    continue

                jobs.append(
                    Job(
                        company=company.title(),
                        job_title=title,
                        location=location,
                        employment_type="",
                        contract_type="Fixed-Term",
                        date_posted="",
                        job_url=job.get("hostedUrl", ""),
                        source="Lever",
                    )
                )

        except Exception as e:
            print(f"{company}: {e}")

    print(f"Lever found {len(jobs)} jobs.")

    return jobs