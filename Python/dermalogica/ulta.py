#import requests
import dryscrape
from bs4 import BeautifulSoup
import pymysql
from vaderSentiment import SentimentIntensityAnalyzer


url="http://www.ulta.com/daily-superfoliant?productId=xlsImpprod15261033"
session=dryscrape.Session()
session.visit(url)
page=session.body()
soup=BeautifulSoup(page,"html.parser")
analyzer = SentimentIntensityAnalyzer()
data=soup.find("div",{"class":"pr-contents-wrapper"})
xyz=[]
for item in data.findAll("div",{"class":"pr-review-wrap"}):
	dict={}
	dict['author']=item.find("p",{"class":"pr-review-author-name"}).find("span").find(text=True)
	dict['loc']=item.find("p",{"class":"pr-review-author-location"}).find("span").find(text=True)
	dict['title']=item.find("p",{"class":"pr-review-rating-headline"}).find(text=True)
	dict['comment']=item.find("p",{"class":"pr-comments"}).find(text=True)
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
	v = i['author']
	w = i['loc']
	x = i['title']
	z = "\"" + i['comment'] + "\""
	u = i['sentiment'] 
	tl = [v,z,u]
	add_review = "INSERT INTO product_reviews(website_name, author, comment, sentiment) VALUES( %s, %s, %s, %s)"
	cursor.execute(add_review, ("ulta",tl[0],tl[1],tl[2]))

cursor.close()

#def close_connection(cursor, con):
con.commit()
con.close()



