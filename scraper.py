import os
from dotenv import load_dotenv
import requests
import csv
from datetime import datetime

load_dotenv()


# Fetch tweets from TwitterAPI.io
API_KEY = os.getenv("twitter_key")
url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
querystring = {"query": "one punch man", "queryType":"Top"}
headers = {"X-API-Key": API_KEY}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

tweets = data.get("tweets", [])
print(f"Fetched {len(tweets)} tweets.")



# Helper for formatting date
def format_date(date_string):
    if not date_string:
        return ""
    try:
        # Convert ISO date to readable format
        date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return date.strftime("%B %d, %Y at %H:%M")
    except:
        return date_string



# Prepare data for CSV
rows = []

for t in tweets:
    rows.append([
        t.get("id", ""),
        t.get("url", ""),
        t.get("text", ""),
        t.get("likeCount", 0),
        t.get("retweetCount", 0),
        t.get("replyCount", 0),
        t.get("quoteCount", 0),
        t.get("viewCount", 0),
        format_date(t.get("createdAt"))
    ])

print(f"Processed {len(rows)} tweets.")


# Write to CSV
CSV_FILENAME = "tweets.csv"

header = [
    "Tweet ID", "URL", "Content", "Likes", "Retweets",
    "Replies", "Quotes", "Views", "Date"
]

with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Saved to {CSV_FILENAME}")
