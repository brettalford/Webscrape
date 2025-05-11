import webscraper as scrape
import dataParsing as process

#input link to news sorted by whatever you want and set to within the last hour for best results
scrape.webscrape("https://www.google.com/search?q=stock+news&sca_esv=74f56c52dd47ad4d&rlz=1C1UEAD_enUS1003US1003&tbs=sbd:1,qdr:h&tbm=nws&sxsrf=AHTn8zohfzcuPkOb_lzMe1HvdNAWZ8Mg7g:1746930323636&source=lnt&sa=X&ved=2ahUKEwj74YzLrpqNAxXB4skDHYxHDE0QpwV6BAgCEAc&biw=1536&bih=791&dpr=1.25")
#output/input csv
process.sortanddisplay('headlines_sentiment.csv')
