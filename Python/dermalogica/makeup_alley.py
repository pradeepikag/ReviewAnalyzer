import requests
import dryscrape
from bs4 import BeautifulSoup
import pymysql
from vaderSentiment import SentimentIntensityAnalyzer

url="https://www.makeupalley.com/product/showreview.asp/ItemId=192371/Daily-Superfoliant/Dermalogica/Scrubs"
session=dryscrape.Session()
session.visit(url)
page=session.body()
soup=BeautifulSoup(page,"html.parser")
analyzer = SentimentIntensityAnalyzer()	

data=soup.find("div",{"id":"reviews-wrapper"})
xyz=[]
for item in data.findAll("div",{"class":"comments"}):
	dict={}
	dict['author']=item.find("div",{"class":"user-name"}).find("p").find(text=True).strip('\t')
	dict['date']=item.find("div",{"class":"date"}).find("p").text.strip('on')
	#dict['user_details']=item.find("div",{"class":"important"}).find("p").find(text=True)
	dict['comment']=item.find("div",{"class":"comment-content"}).find("p").find(text=True)
	vs = analyzer.polarity_scores(dict['comment'])
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
	#w = i['loc']
	#x = i['title']
	z = "\"" + i['comment'] + "\""
	u = i['sentiment'] 
	tl = [v,z,u]
	add_review = "INSERT INTO product_reviews(website_name, author, comment, sentiment) VALUES( %s, %s, %s, %s)"
	cursor.execute(add_review, ("makeup_alley",tl[0],tl[1],tl[2]))

cursor.close()

#def close_connection(cursor, con):
con.commit()
con.close()

