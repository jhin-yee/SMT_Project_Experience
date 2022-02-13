import json
import os
import time
from datetime import datetime, timezone

import pytz
import requests
import telegram_send
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Change to file directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Add logger configurations
logger.add(
    "../../../logs/scraper/reddit/historical_scraper.log",
    format="{time} {file} {level} {message}",
    level="DEBUG",
)

# Constants
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))


def monthly_crawl_submissions():
    OUTPUT_DIR = "./data"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    telegram_send.send(
        messages=[f"REDDIT HISTORICAL --> Submissions crawling started at {datetime.now(TIMEZONE)}"]
    )

    # Start scraping from given date
    last_created_utc = os.getenv("SCRAPE_FROM_DATE")
    while True:
        logger.debug(f"last_created_utc: {last_created_utc}")
        params = {
            "subreddit": "singapore",
            "sort": "asc",
            "metadata": "true",
            "after": last_created_utc,
            "size": 100,  # Max 500
        }

        try:
            response = requests.get(
                "https://api.pushshift.io/reddit/search/submission/", params=params
            )

            if response.status_code == 200:
                jobj = json.loads(response.text)
                if jobj.get("data"):
                    for submission in jobj.get("data"):
                        created_utc = submission["created_utc"]
                        yyyymm = datetime.fromtimestamp(created_utc, timezone.utc).strftime("%Y%m")
                        with open(f"{OUTPUT_DIR}/{yyyymm}.jsonl", "a") as fo:
                            fo.write(json.dumps(submission) + "\n")

                    logger.debug(f"Data size: {len(jobj.get('data'))}")
                    last_created_utc = jobj["data"][-1]["created_utc"]

                    time.sleep(3)
                else:
                    logger.debug("No data in submission object.")
                    break

        except Exception as e:
            logger.exception(e)
            telegram_send.send(messages=[f"Error occured, retrying.\n{e}"])
            time.sleep(15)
            continue
    logger.debug("Submissions crawling complete.")
    telegram_send.send(messages=["REDDIT HISTORICAL --> Submissions crawling completed."])
