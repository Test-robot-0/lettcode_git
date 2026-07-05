from playwright.sync_api import sync_playwright
import json
import config
import database.repository as repository

def get_question(title_slug, current_id):

    URL = f"{config.QUESTION_URL}{title_slug}/description"
    
    
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
    
        page.goto(URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        page.screenshot(path="page.png", full_page=True)
        
        next_data = page.locator("#__NEXT_DATA__").text_content()
        json_data = json.loads(next_data) 
   

        if next_data:
            question = json_data["props"]["pageProps"]["dehydratedState"]["queries"][1]["state"]["data"]["question"]["content"]
            stats = json_data["props"]["pageProps"]["dehydratedState"]["queries"][1]["state"]["data"]["question"]["stats"]
            
            repository.update_question(question, stats, current_id)
                 
        else:
            print("__NEXT_DATA__ not found")

        browser.close()
        repository.commit()
    
    print("(4/7) Done getting question")
    
        
