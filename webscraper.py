from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from playwright.sync_api import sync_playwright

pw=sync_playwright().start()

browser = pw.firefox.launch()

page=browser.new_page()
page.goto("http://google.com")

print(page.content())
page.screenshot(path="example.png")


browser.close