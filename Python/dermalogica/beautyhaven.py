import requests
import dryscrape
from bs4 import BeautifulSoup
#from vaderSentiment import SentimentIntensityAnalyzer

url="https://www.beautyheaven.com.au/skin-care/face-scrubs-exfoliators-peels/product/daily-superfoliant"

session=dryscrape.Session()
session.visit(url)
page=session.body()
soup=BeautifulSoup(page,"html.parser")


#analyzer = SentimentIntensityAnalyzer()	
#soup = scrape_start(url)
data=soup.findAll("div",{"class":"view-content"})

xyz=[]
for item in data.findAll("div",{"class":"node-product_review teaser clerafix"}):
	dict={}
	dict['author']=item.find("h4").find("span",{"class":"username level-silver"}).find(text=True)
	"""dict['loc']=item.find("p",{"class":"pr-review-author-location"}).find("span").find(text=True)
	dict['title']=item.find("h4").find(text=True)
	dict['comment']=item.find("div",{"class":"field-items"}).find(text=True)
	vs = analyzer.polarity_scores(dict['comment'])
	dict['sentiment'] = str(vs)""" 	
	xyz.append(dict)
	
print(xyz)


