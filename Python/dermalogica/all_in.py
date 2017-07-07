import dryscrape
from bs4 import BeautifulSoup
from vaderSentiment import SentimentIntensityAnalyzer

class Adorebeauty(object):
	url="https://www.adorebeauty.com.au/dermalogica/dermalogica-daily-superfoliant.html"
	session=dryscrape.Session()
	session.visit(url)
	page=session.body()
	soup=BeautifulSoup(page,"html.parser")
	analyzer = SentimentIntensityAnalyzer()	
	data=soup.find("div",{"id":"customer-reviews"})
	xyz=[]
	for item in data.findAll("div",{"itemprop":"review"}):
		dict={}
		dict['user']=item.find("span",{"itemprop":"author"}).find(text=True)
		dict['review_title']=item.find("span",{"class":"review-title"}).find(text=True)	
		dict['date']=item.find("span",{"class":"date"}).find(text=True)	
		dict['comments']=item.find("p",{"itemprop":"description"}).find(text=True)
		vs = analyzer.polarity_scores(dict['comment'])
		#print(str(vs))
		dict['sentiment'] = str(vs) 	
		xyz.append(dict)
	return xyz

class Makeup_alley():
	url="https://www.makeupalley.com/product/showreview.asp/ItemId=192371/Daily-Superfoliant/Dermalogica/Scrubs"
	session=dryscrape.Session()
	session.visit(url)
	page=session.body()
	soup=BeautifulSoup(page,"html.parser")

	data=soup.find("div",{"id":"reviews-wrapper"})
	xyz=[]
	for item in data.findAll("div",{"class":"comments"}):
		dict={}
		dict['author']=item.find("div",{"class":"user-name"}).find("p").find(text=True).strip('\t')
		dict['date']=item.find("div",{"class":"date"}).find("p").text.strip('on')
		dict['user_details']=item.find("div",{"class":"important"}).find("p").find(text=True)
		dict['comment']=item.find("div",{"class":"comment-content"}).find("p").find(text=True)
		#dict['points']=item.find("div",{"class":"pr-review-points"}).find(text=True)
		#dict['date']=item.find("div",{"class":"pr-review-rating-wrapper"}).find("div",{"class":"pr-review-author pr-rounded"}).find(text=True)
		xyz.append(dict)
	
	print(xyz)

class Nykaa():
	url="https://www.makeupalley.com/product/showreview.asp/ItemId=192371/Daily-Superfoliant/Dermalogica/Scrubs"
	session=dryscrape.Session()
	session.visit(url)
	page=session.body()
	soup=BeautifulSoup(page,"html.parser")

	data=soup.find("div",{"id":"reviews-wrapper"})
	xyz=[]
	for item in data.findAll("div",{"class":"comments"}):
		dict={}
		dict['author']=item.find("div",{"class":"user-name"}).find("p").find(text=True).strip('\t')
		dict['date']=item.find("div",{"class":"date"}).find("p").text.strip('on')
		dict['user_details']=item.find("div",{"class":"important"}).find("p").find(text=True)
		dict['comment']=item.find("div",{"class":"comment-content"}).find("p").find(text=True)
		xyz.append(dict)
	print(xyz)
