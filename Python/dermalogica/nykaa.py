import requests
import dryscrape
from bs4 import BeautifulSoup
from vaderSentiment import SentimentIntensityAnalyzer
import pymysql
 
url="http://www.nykaa.com/dermalogica-daily-superfoliant.html?ptype=product&id=127569?&root=search&searchterm=dermalogica%20superfoliant&type=product"
session=dryscrape.Session()
session.visit(url)
page=session.body()
soup=BeautifulSoup(page,"html.parser")
#return soup

analyzer = SentimentIntensityAnalyzer()	
data=soup.find("div",{"id":"customer-reviews"})
xyz=[]
for item in data.findAll("div",{"class":"product-tab-reviews"}):
	dict={}
	dict['author']=item.find("div",{"class":"r-name"}).find("p").find(text=True)
	#k=item.find("div",{"class":"r-detail"}).find(text=True)
	dict['title']=item.find("div",{"class":"r-detail"}).find("p",{"class":"r-heading"}).find(text=True)
	dict['comment']=item.find("div",{"class":"r-detail"}).find("p").find(text=True)
	vs = analyzer.polarity_scores(dict['comment'])	
	dict['sentiment'] = str(vs) 
	#print(dict[comment],sen)		
	dict['date']=item.find("div",{"class":"r-detail"}).find("p",{"class":"posted-date"}).text
	xyz.append(dict)
#print(xyz)
con = pymysql.connect(user='root', password='pradeepika', database='customerreviews', charset='utf8') 
cursor = con.cursor()
DB_NAME = 'customerreviews'

for i in xyz:
	v = i['author']
	#w = i['loc']
	x = i['title']
	z = "\"" + i['comment'] + "\""
	u = i['sentiment'] 
	tl = [v,x,z,u]
	add_review = "INSERT INTO product_reviews(website_name, author, title, comment, sentiment) VALUES( %s, %s, %s, %s, %s)"
	cursor.execute(add_review, ("nykaa",tl[0],tl[1],tl[2],tl[3]))

cursor.close()

#def close_connection(cursor, con):
con.commit()
con.close()


