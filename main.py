from sheets import connect_sheet
from scrapers import (
    scrape_recruitee,
    scrape_greenhouse,
    scrape_lever,
    scrape_workable,
    scrape_ashby,
)


def create_headers(sheet):

    headers = [
        "Company",
        "Job Title",
        "Location",
        "Employment Type",
        "Contract Type",
        "Date Posted",
        "Job URL",
        "Source",
    ]

    if sheet.row_values(1) != headers:
        sheet.clear()
        sheet.append_row(headers)


def job_exists(sheet, job_url):

    urls = sheet.col_values(7)  # Job URL column

    return job_url in urls


def main():

    sheet = connect_sheet()

    create_headers(sheet)

    jobs = []

    jobs.extend(scrape_recruitee())
    jobs.extend(scrape_greenhouse())
    jobs.extend(scrape_lever())
    jobs.extend(scrape_workable())
    jobs.extend(scrape_ashby())

    added = 0

    for job in jobs:

        if job_exists(sheet, job.job_url):
            continue

        sheet.append_row([
            job.company,
            job.job_title,
            job.location,
            job.employment_type,
            job.contract_type,
            job.date_posted,
            job.job_url,
            job.source,
        ])

        added += 1

    print(f"Added {added} jobs to Google Sheets.")


if __name__ == "__main__":
    main()