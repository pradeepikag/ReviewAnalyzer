import requests
import dryscrape
from bs4 import BeautifulSoup
#from vaderSentiment import SentimentIntensityAnalyzer
url="https://www.yelp.com/biz/dermalogica-san-francisco-2"
session=dryscrape.Session()
session.visit(url)
page=session.body()
soup=BeautifulSoup(page,"html.parser")
#return soup

#def scrape_in_dictformat():
#analyzer = SentimentIntensityAnalyzer()	
#soup = scrape_start(url)
#data=soup.find("div",{"class":"review-list"})
#x=data.find("ul",{"class":"ylist ylist-bordered reviews"})
xyz=[]
for item in soup.findAll("div",{"class":"review review--with-sidebar"}):
	dict = {}
	#dict["user_name"] = item.find("div",{"class":"review-sidebar"}).find("div",{"class":"review-sidebar-content"}).find("div",{"class":"media-story"}).find("li",{"class":"user-name"}).find(text=True)					
	#dict["location"] = r.find("li",{"class":"user-location responsive-hidden-small"}).find(text=True)
	#dict["date"] = r.find("div",{"class":"review-content"}).find("span",{"rating-qualifier"}).find(text=True)
	dict["content"] = item.find("p",{"lang":"en"}).find(text=True)
	xyz.append(dict)
print(xyz)
