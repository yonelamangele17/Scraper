import requests
from bs4 import BeautifulSoup

from utils.job import Job

URL = "https://www.electrumsoftware.com/careers"


def scrape():

    jobs = []

    response = requests.get(URL, timeout=15)

    if response.status_code != 200:
        return jobs

    with open("data/electrum.html", "w", encoding="utf-8") as file:
        file.write(response.text)

    print("✅ Electrum HTML saved.")

    return jobs