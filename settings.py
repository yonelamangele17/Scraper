from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Credentials
CREDENTIALS_FILE = BASE_DIR / "credentials" / "service_account.json"

# Google Sheet
SPREADSHEET_NAME = "Software Jobs"
WORKSHEET_NAME = "Sheet1"

# Search Settings
SEARCH_KEYWORDS = [
    "Full Stack Developer",
    "Software Developer",
    "Web Developer",
    "Front-End Developer",
    "Back-End Developer",
    "Python Developer"
]

SEARCH_LOCATIONS = [
    "Cape Town",
    "Remote",
    "South Africa"
]