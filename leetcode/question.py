import json
import config
import database.repository as repository
import requests

def get_question(title_slug, current_id):

    GRAPHQL_URL = config.GRAPHQL_URL
    QUERY = config.QUERY

    r = requests.post(
        GRAPHQL_URL,
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
        },
        json={
            "query": QUERY,
            "variables": {
                "titleSlug": title_slug
            }
        },
        timeout=30,
    )

    if r.status_code == 200:
        data = r.json()
        
        question = data["data"]["question"]["content"]
        stats = data["data"]["question"]["stats"]

        repository.update_question(question, stats, current_id)

    else:
        print("Error code", r.status_code)

    print("(4/7) Done getting question", r.status_code)
    
