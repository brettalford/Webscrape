from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from playwright.sync_api import sync_playwright
import re
import time

analyzer = SentimentIntensityAnalyzer()

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

#number of pages to search
max_pages = 10  
#scores overall
scores=[]
#aggregte score
aggscore=0

#starting up playwright
with sync_playwright() as p:
    #launching chromiun
    browser = p.chromium.launch(headless=True)
    #page is a new page
    page = browser.new_page()

    #youll change this url to the news topic you want
    base_url = "https://www.google.com/search?q=github&sca_esv=a122d3f84a806bce&rlz=1C1UEAD_enUS1003US1003&tbs=sbd:1,qdr:d&tbm=nws&sxsrf=AHTn8zrhVtNdlg-uyXid4Qm0HWMEggu2rg:1746689853072&source=lnt&sa=X&ved=2ahUKEwjPqebhrpONAxVj4skDHazQNSYQpwV6BAgCEAg&biw=1536&bih=791&dpr=1.25"
    #
    #
    #telling playwright to go to this url
    page.goto(base_url)

    #for the number of pages
    for i in range(max_pages):
        #page increment
        current_page = i + 1
        #print page num
        print(f"\n--- Page {current_page} ---\n")

        #try to select a headline element
        try:
            page.wait_for_selector("div.n0jPhd", timeout=3000)  
            headlines = page.query_selector_all("div.n0jPhd")

            #if you cant find another
            if not headlines:  
                print("No headlines found on this page.")
                break

            #extracting hedline stuffs and adding scores based on sentiment analysis via vader
            for h in headlines:
                raw_text = h.inner_text().strip()
                text = clean_text(raw_text)
                score = analyzer.polarity_scores(text)['compound']
                print(f"{text} — {score:.3f}")
                scores.append(score)
                aggscore+=score
        #exception
        except Exception as e:
            print(f"Error occurred: {e}")
            break


        #go to th next page via the number at the bottom
        next_page_label = f"a[aria-label='Page {current_page + 1}']"
        if page.locator(next_page_label).is_visible():
            page.click(next_page_label)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)
        #if there isnt another page and you havent reached your total pages
        else:
            print("No more pages.")
            break
    
    browser.close()

#final scores
finalscore=aggscore/len(scores)
print (scores)
print(f'final score {finalscore}')