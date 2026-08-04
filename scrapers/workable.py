import json
import requests

from config.companies import (
    WORKABLE_COMPANIES,
    KEYWORDS,
    LOCATIONS,
)

from utils.job import Job


def scrape():

    jobs = []

    print("\n========== WORKABLE ==========")

    total = 0

    for company, account_id in WORKABLE_COMPANIES.items():

        company_count = 0

        url = (
            f"https://apply.workable.com/api/v1/widget/accounts/"
            f"{account_id}?origin=embed&callback=whrcallback"
        )

        try:

            response = requests.get(url, timeout=15)

            if response.status_code != 200:
                print(f"{company:<20}: HTTP {response.status_code}")
                continue

            text = response.text

            text = text.replace("/**/whrcallback(", "")
            text = text[:-1]

            data = json.loads(text)

            for job in data.get("jobs", []):

                title = job.get("title", "")
                location = job.get("city", "")

                if not any(word in title.lower() for word in KEYWORDS):
                    continue

                if not any(place in location.lower() for place in LOCATIONS):
                    continue

                company_count += 1
                total += 1

                jobs.append(
                    Job(
                        company=company,
                        job_title=title,
                        location=location,
                        employment_type=job.get("employment_type", ""),
                        contract_type="Fixed-Term",
                        date_posted=job.get("published_on", ""),
                        job_url=job.get("url", ""),
                        source="Workable",
                    )
                )

            print(f"{company:<20}: {company_count}")

        except Exception as e:
            print(f"{company}: {e}")

    print(f"\nWorkable Total: {total}\n")

    return jobs