import requests

from utils.job import Job

from config.companies import (
    GREENHOUSE_COMPANIES,
    KEYWORDS,
    LOCATIONS
)


def scrape():

    jobs = []

    for board in GREENHOUSE_COMPANIES:

        url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"

        try:
            response = requests.get(url, timeout=15)

            if response.status_code != 200:
                continue

            data = response.json()

            for job in data.get("jobs", []):

                title = job.get("title", "")
                location = job.get("location", {}).get("name", "")

                if not any(word in title.lower() for word in KEYWORDS):
                    continue

                if not any(place in location.lower() for place in LOCATIONS):
                    continue

                jobs.append(
                    Job(
                        company=board.title(),
                        job_title=title,
                        location=location,
                        employment_type="",
                        contract_type="Fixed-Term",
                        date_posted="",
                        job_url=job.get("absolute_url", ""),
                        source="Greenhouse",
                    )
                )

        except Exception as e:
            print(f"{board}: {e}")

    print(f"Greenhouse found {len(jobs)} jobs.")

    return jobs