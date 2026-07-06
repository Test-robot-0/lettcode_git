from playwright.sync_api import sync_playwright
import json
import config
import database.repository as repository
import requests

def get_question(title_slug, current_id):

    URl = f"https://alfa-leetcode-api.onrender.com/select/raw?titleSlug={title_slug}"

    r = requests.get(URl)
    
    if r.status_code == 429:
        print(r.content)
        print("Error in question")
        repository.error_update_1()
        

    if r.status_code == 200:
        data = r.json()
        
        question = data["question"]["content"]
        stats = data["question"]["stats"]

        repository.update_question(question, stats, current_id)
    
    else:
        print("Error code", r.status_code)

    print("(4/7) Done getting question", r.status_code)

