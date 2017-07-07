import requests
import dryscrape
import pymysql
from bs4 import BeautifulSoup
from vaderSentiment import SentimentIntensityAnalyzer

url="https://www.sohoskincare.com.au/dermalogica-age-smart-daily-superfoliant-57g"
session = dryscrape.Session()
session.visit(url)
page = session.body()
soup=BeautifulSoup(page,"html.parser")
analyzer = SentimentIntensityAnalyzer()
data=soup.findAll("form",{"id":"form-review"})

xyz=[]
for item in data:
     dict = {}
     dict["date"]=item.find("td",{"class":"text-right"}).find(text=True)
     dict["author"]=item.find("strong").find(text=True)
     dict["comment"]=item.find("p").find(text=True)
     vs = analyzer.polarity_scores(dict['comment'])
     #print(str(vs))
     dict['sentiment'] = str(vs)
     xyz.append(dict)
#print(list)
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
	cursor.execute(add_review, ("Soho_skincare",tl[0],tl[1],tl[2]))

cursor.close()

#def close_connection(cursor, con):
con.commit()
con.close()

