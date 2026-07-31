from dataclasses import dataclass


@dataclass
class Job:
    company: str
    job_title: str
    location: str
    employment_type: str
    contract_type: str
    date_posted: str
    job_url: str
    source: str