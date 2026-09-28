import requests
import json
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


# HackerNews API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# User-Agent required by the assignment
headers = {
    "User-Agent": "TrendPulse/1.0"
}


# Keywords for each category
keywords = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}


# Get the top 500 story IDs
try:
    response = requests.get(
        TOP_STORIES_URL,
        headers=headers,
        timeout=10
    )
    response.raise_for_status()

    story_ids = response.json()[:500]

    print("Fetched", len(story_ids), "story IDs.")

except requests.RequestException as error:
    print("Failed to fetch story IDs:", error)
    exit()


# Function to fetch one story
def fetch_story(story_id):
    try:
        url = ITEM_URL.format(story_id)

        response = requests.get(
            url,
            headers=headers,
            timeout=5
        )

        response.raise_for_status()

        story = response.json()

        if story and story.get("type") == "story" and story.get("title"):
            return story

    except requests.RequestException:
        print("Failed to fetch story:", story_id)

    return None


# Fetch stories using several requests at the same time
stories = []

with ThreadPoolExecutor(max_workers=10) as executor:

    futures = [
        executor.submit(fetch_story, story_id)
        for story_id in story_ids
    ]

    for future in as_completed(futures):

        story = future.result()

        if story is not None:
            stories.append(story)


print("Successfully fetched", len(stories), "stories.")


# Store stories by category
collected = {
    "technology": [],
    "worldnews": [],
    "sports": [],
    "science": [],
    "entertainment": []
}


# Process each category
for category, words in keywords.items():

    print()
    print("Processing category:", category)

    for story in stories:

        # Stop after collecting 25 stories
        if len(collected[category]) >= 25:
            break

        title = story.get("title", "")

        # Check each keyword
        for word in words:

            if word.lower() in title.lower():

                story_data = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().isoformat()
                }

                collected[category].append(story_data)

                break

    print(
        category,
        "stories collected:",
        len(collected[category])
    )

    # Required 2-second wait between categories
    time.sleep(2)


# Combine all stories
all_stories = []

for category in collected:
    all_stories.extend(collected[category])


# Create data folder
os.makedirs("data", exist_ok=True)


# Create today's filename
date_string = datetime.now().strftime("%Y%m%d")

filename = f"data/trends_{date_string}.json"


# Save stories to JSON
with open(filename, "w", encoding="utf-8") as file:

    json.dump(
        all_stories,
        file,
        indent=4,
        ensure_ascii=False
    )


# Print final result
print()
print("Category totals:")

for category in collected:
    print(
        category,
        ":",
        len(collected[category])
    )

print()
print(
    f"Collected {len(all_stories)} stories. "
    f"Saved to {filename}"
)