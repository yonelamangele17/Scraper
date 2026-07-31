import requests

from utils.job import Job
from config.companies import (
    RECRUITEE_COMPANIES,
    KEYWORDS,
    LOCATIONS,
)


def scrape():

    jobs = []

    for company in RECRUITEE_COMPANIES:

        url = f"https://{company}.recruitee.com/api/offers/"

        try:

            response = requests.get(url, timeout=20)

            if response.status_code != 200:
                continue

            data = response.json()

            for offer in data.get("offers", []):

                title = offer.get("title", "")
                location = offer.get("location", "") or offer.get("country", "")

                if not any(word in title.lower() for word in KEYWORDS):
                    continue

                location_text = str(location).lower()

                if not any(place in location_text for place in LOCATIONS):
                    continue

                jobs.append(
                    Job(
                        company=company.title(),
                        job_title=title,
                        location=location,
                        employment_type="",
                        contract_type="Fixed-Term",
                        date_posted=offer.get("published_at", ""),
                        job_url=offer.get("careers_url", ""),
                        source="Recruitee",
                    )
                )

        except Exception as e:
            print(f"{company}: {e}")

    print(f"Recruitee found {len(jobs)} jobs.")

    return jobs