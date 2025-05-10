from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from playwright.sync_api import sync_playwright
import re
import time
import csv
from datetime import datetime

analyzer = SentimentIntensityAnalyzer()

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

#number of pages to search
max_pages = 5  
#scores overall
scores=[]
#aggregte score
aggscore=0
#zeros removed
filteredscore=0
#date
date = datetime.now()
#headlines
headstore=[]
#links
links=[]
#pagelinks
pagelinks=[]
#relative times
reltimes=[]



#starting up playwright
with sync_playwright() as p:
    #launching chromiun
    browser = p.chromium.launch(headless=True)
    #page is a new page
    page = browser.new_page()

    #youll change this url to the news topic you want
    base_url = "https://www.google.com/search?q=us+stock+market&sca_esv=31cd4d2547bda482&rlz=1C1UEAD_enUS1003US1003&tbs=sbd:1,qdr:h&tbm=nws&sxsrf=AHTn8zreex89nP19iZt2jxqvOFPypdkCYg:1746816456683&source=lnt&sa=X&ved=2ahUKEwjivY2zhpeNAxWTLtAFHQxsE5UQpwV6BAgCEAc&biw=1536&bih=791&dpr=1.25"
    #
    #
    #
    #telling playwright to go to this url
    page.goto(base_url)

    #for the number of pages
    for i in range(max_pages):
        #page increment
        current_page = i + 1
        #print page num
        #print(f"\n--- Page {current_page} ---\n")

        #try to select a headline element
        try:
            page.wait_for_selector("div.n0jPhd", timeout=1250)  
            headlines = page.query_selector_all("div.n0jPhd")
            link_elements = page.query_selector_all("a.WlydOe")
            page_times = page.query_selector_all("div.OSrXXb.rbYSKb.LfVVr > span")

            for link in link_elements:
                href = link.get_attribute("href")
                links.append(href)

            for times in page_times:
                time_text = times.text_content()
                reltimes.append(time_text)
            #if you cant find another
            if not headlines:  
                print("No headlines found on this page.")
                break


            #extracting hedline stuffs and adding scores based on sentiment analysis via vader
            for h in headlines:
                raw_text = h.inner_text().strip()
                text = clean_text(raw_text)
                score = analyzer.polarity_scores(text)['compound']
                #print(f"{text} — {score:.3f}")
                scores.append(score)
                headstore.append(text)
                aggscore+=score
        #exception
        except Exception as e:
            print(f"Error occurred: {e}")
            break


        #go to the next page via the number at the bottom
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


scorecount=0
#final scores
for i in range(len(scores)):
    if(scores[i]!=0.0):
        filteredscore+=(scores[i])
        scorecount+=1
finalscore=aggscore/len(scores)
#print (scores)
#print(f'final score {finalscore}')
#print(f'filtered score {filteredscore/(scorecount)}')
#print(f'times: {reltimes}')


#writing headlines and scores to csv
with open('headlines_sentiment.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Headline', 'Links', 'Sentiment Score', 'Upload Date', 'Relative time'])  # Updated header
    for i in range(len(headstore)):
        writer.writerow([headstore[i], links[i], scores[i], date, reltimes[i]])
