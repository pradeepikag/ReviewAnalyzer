import requests
import dryscrape
from bs4 import BeautifulSoup
#from vaderSentiment import SentimentIntensityAnalyzer

def scrape_start():
	url="http://www.dermalogica.co.uk/uk/html/products/daily-superfoliant-229.html"
	session = dryscrape.Session()
	session.set_timeout(60)
	session.visit(url)
	page = session.body()
	soup = BeautifulSoup(page,'html.parser')
	return soup

def scrape_in_dictformat():
	#analyzer = SentimentIntensityAnalyzer()	
	sam = scrape_start()
	data =sam.find("div",{"class":"pr-contents-wrapper"})
	xyz=[]
	for item in data.findAll("div",{"class":"pr-review-wrap"}):
		dict={}
		dict['author']=item.find("p",{"class":"pr-review-author-name"}).find("span").find(text=True)
		dict['loc']=item.find("p",{"class":"pr-review-author-location"}).find("span").find(text=True)
		dict['title']=item.find("div",{"class":"pr-review-rating"}).find("p",{"class":"pr-review-rating-headline"}).find(text=True)
		dict['comment']=item.find("div",{"class":"pr-review-text"}).find("p",{"class":"pr-comments"}).find(text=True)
		#vs = analyzer.polarity_scores(dict['comment'])
		#print(str(vs))
		#dict['sentiment'] = str(vs) 
		#print(dict[comment],sen)		
		dict['age_grp']=(item.find("li",{"class":"pr-other-attribute-value"}).text)
		xyz.append(dict)
	return xyz;	
	print(xyz)


