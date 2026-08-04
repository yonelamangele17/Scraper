import requests

from utils.job import Job

from config.companies import (
    GREENHOUSE_COMPANIES,
    KEYWORDS,
    LOCATIONS
)


def scrape():

    jobs = []

    print("\n========== GREENHOUSE ==========")

    total = 0

    for company_name, board in GREENHOUSE_COMPANIES.items():

        company_count = 0

        url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"

        try:
            response = requests.get(url, timeout=15)

            if response.status_code != 200:
                print(f"{board:<20}: HTTP {response.status_code}")
                continue

            data = response.json()

            for job in data.get("jobs", []):

                title = job.get("title", "")
                location = job.get("location", {}).get("name", "")

                if not any(word in title.lower() for word in KEYWORDS):
                    continue

                if not any(place in location.lower() for place in LOCATIONS):
                    continue

                company_count += 1
                total += 1

                jobs.append(
                    Job(
                        company=company_name,
                        job_title=title,
                        location=location,
                        employment_type="",
                        contract_type="Fixed-Term",
                        date_posted="",
                        job_url=job.get("absolute_url", ""),
                        source="Greenhouse",
                    )
                )

            print(f"{company_name:<20}: {company_count}")

        except Exception as e:
            print(f"{board:<20}: ERROR ({e})")

    print(f"\nGreenhouse Total: {total}\n")

    return jobs