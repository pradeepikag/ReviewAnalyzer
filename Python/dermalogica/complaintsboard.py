import requests
import dryscrape
from bs4 import BeautifulSoup
#import pymysql
from vaderSentiment import SentimentIntensityAnalyzer

url="https://www.complaintsboard.com/?search=dermalogica"
session=dryscrape.Session()
session.visit(url)
page=session.body()
soup=BeautifulSoup(page,"html.parser")
analyzer = SentimentIntensityAnalyzer()
data=soup.find("div",{"class":"col-main"})
xyz=[]
for item in data.findAll("div",{"class":"item-row",}):
	dict={}
	if item.table is None:
		continue
	dict["title"]=item.table.find("td",{"class":"complaint"}).h4.a.text
	dict["author"]=item.table.find("table").find("td",{"class":"small"}).a.text
	dict["comment"]=item.table.find("td",{"class":"compl-text"}).div.text
	vs = analyzer.polarity_scores(dict['comment'])
	dict['sentiment'] = str(vs) 
	xyz.append(dict)
print(xyz)

"""con = pymysql.connect(user='root', password='pradeepika', database='customerreviews', charset='utf8')    
cursor = con.cursor()
DB_NAME = 'customerreviews'


sql="CREATE TABLE product_reviews(sno INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(sno), website_name VARCHAR(100) NOT NULL, title VARCHAR(200), loc VARCHAR(100),date DATE, comment TEXT NOT NULL, sentiment VARCHAR(200) NOT NULL)"

cursor.execute(sql)
for i in xyz:
	x = i['title']
	z = "\"" + i['comment'] + "\""
	#vs = analyzer.polarity_scores(i['comment'])
	#print(str(vs))
	#sen = str(vs)
	u = i['sentiment'] 
	tl = [x,z,u]
	add_review = "INSERT INTO product_reviews(website_name, title, comment, sentiment) VALUES(%s, %s, %s, %s)"
	cursor.execute(add_review, ("complaints_board",tl[0],tl[1],tl[2]))

cursor.close()

#def close_connection(cursor, con):
con.commit()
con.close()

"""

