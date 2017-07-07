import requests
import dryscrape
from bs4 import BeautifulSoup
from vaderSentiment import SentimentIntensityAnalyzer
import pymysql

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
	dict['author']=item.find("span",{"itemprop":"author"}).find(text=True)
	dict['title']=item.find("span",{"class":"review-title"}).find(text=True)	
	dict['date']=item.find("span",{"class":"date"}).find(text=True)	
	dict['comment']=item.find("p",{"itemprop":"description"}).find(text=True)
	vs = analyzer.polarity_scores(dict['comment'])
	#print(str(vs))
	dict['sentiment'] = str(vs) 	
	#dict['points']=item.find("div",{"class":"pr-review-points"}).find(text=True)
	#dict['date']=item.find("div",{"class":"pr-review-rating-wrapper"}).find("div",{"class":"pr-review-author pr-rounded"}).find(text=True)
	xyz.append(dict)
	
#print(xyz)
con = pymysql.connect(user='root', password='pradeepika', database='customerreviews', charset='utf8')    
cursor = con.cursor()
DB_NAME = 'customerreviews'

for i in xyz:
	w = i['author']
	x = i['title']	
	#v = i['date']
	z = "\"" + i['comment'] + "\""
	u = i['sentiment'] 
	tl = [w,x,z,u]
	add_review = "INSERT INTO product_reviews(website_name, author, title, comment, sentiment) VALUES (%s, %s, %s, %s, %s)"
	cursor.execute(add_review, ("adore_beauty",tl[0],tl[1],tl[2],tl[3]))

cursor.close()

#def close_connection(cursor, con):
con.commit()
con.close()
