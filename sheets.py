import gspread
from google.oauth2.service_account import Credentials

from settings import (
    CREDENTIALS_FILE,
    SPREADSHEET_NAME,
    WORKSHEET_NAME
)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def connect_sheet():
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=SCOPES
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open(SPREADSHEET_NAME)

    worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

    return worksheet

from utils.job import Job


def append_jobs(sheet, jobs: list[Job]):

    rows = []

    for job in jobs:

        rows.append([
            job.company,
            job.job_title,
            job.location,
            job.employment_type,
            job.contract_type,
            job.date_posted,
            job.job_url,
            job.source
        ])

    if rows:
        sheet.append_rows(rows)