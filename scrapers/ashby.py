import requests

from utils.job import Job
from config.companies import (
    ASHBY_COMPANIES,
    KEYWORDS,
    LOCATIONS,
)


def scrape_ashby():

    jobs = []

    print("\n========== ASHBY ==========")

    total = 0

    for company in ASHBY_COMPANIES:

        company_count = 0

        url = f"https://api.ashbyhq.com/posting-api/job-board/{company}"

        try:

            response = requests.get(url, timeout=15)

            if response.status_code != 200:
                print(f"{company:<20}: HTTP {response.status_code}")
                continue

            data = response.json()

            all_jobs = data.get("jobs", [])

            print(f"{company:<20}: {len(all_jobs)} total postings")

            for job in all_jobs:

                title = job.get("title", "")
                location = job.get("location", "")

                if not any(word in title.lower() for word in KEYWORDS):
                    continue

                location_text = str(location).lower()

                if not any(place in location_text for place in LOCATIONS):
                    continue

                company_count += 1
                total += 1

                jobs.append(
                    Job(
                        company=company.title(),
                        job_title=title,
                        location=location,
                        employment_type=job.get("employmentType", ""),
                        contract_type="Fixed-Term",
                        date_posted=job.get("publishedAt", ""),
                        job_url=job.get("jobUrl", ""),
                        source="Ashby",
                    )
                )

            print(f"{company:<20}: {company_count}")

        except Exception as e:
            print(f"{company}: {e}")

    print(f"\nAshby Total: {total}\n")

    return jobs