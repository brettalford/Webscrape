from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from playwright.sync_api import sync_playwright
import re
import time
import csv
from datetime import datetime
def clean_text(text):
        return re.sub(r'[^\x00-\x7F]+', '', text)

def webscrape(link):
    analyzer = SentimentIntensityAnalyzer()
    #number of pages to search(no reason not to do max)
    max_pages = 50  
    #scores overall
    scores=[]
    #aggregte score
    aggscore=0
    #zeros removed
    filteredscore=0
    #current uplod time
    now = datetime.now()
    uptime = now.hour * 60 + now.minute
    #headlines
    headstore=[]
    #links
    links=[]
    #pagelinks
    pagelinks=[]
    #relative times
    reltimes=[]
    #absolute time
    abstime=[]



    #starting up playwright
    with sync_playwright() as p:
        #launching chromiun
        browser = p.chromium.launch(headless=True)
        #context to make it seem more normal to google algo
        context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 768},
        locale="en-US"
        )
        page = context.new_page()


        #youll change this url to the news topic you want
        base_url = link 
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
                page.wait_for_selector("div.n0jPhd", timeout=1500)  
                headlines = page.query_selector_all("div.n0jPhd")
                link_elements = page.query_selector_all("a.WlydOe")
                page_times = page.query_selector_all("div.OSrXXb.rbYSKb.LfVVr > span")
                #getting links
                for link in link_elements:
                    href = link.get_attribute("href")
                    links.append(href)
                #getting relative and absolute times
                for times in page_times:
                    time_text = times.text_content()
                    match = re.search(r'\d+', time_text)
                    reltimes.append(int(match.group()) if match else 0)
                    abstime.append(uptime-(int(match.group()) if match else 0))
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
    print(f'final score {finalscore}')
    print(f'filtered score {filteredscore/(scorecount)}')
    #print(f'times: {reltimes}')


    #writing headlines and scores to csv
    with open('headlines_sentiment.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        #only needs to run the first time
        writer.writerow(['Headline', 'Links', 'Sentiment Score', 'Upload Date', 'Relative Time', 'Absolute Time']) 
        #writing data 
        for i in range(len(headstore)):
            writer.writerow([headstore[i], links[i], scores[i], uptime, reltimes[i], abstime[i]])
    file.close()

