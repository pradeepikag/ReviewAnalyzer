import requests
import dryscrape
import pymysql
from bs4 import BeautifulSoup
from vaderSentiment import SentimentIntensityAnalyzer

url="https://www.lookfantastic.com/dermalogica-daily-superfoliant-57g/11388132.html"
session=dryscrape.Session()
session.visit(url)
page=session.body()
soup=BeautifulSoup(page,"html.parser")
#return soup

#def scrape_in_dictformat():
analyzer = SentimentIntensityAnalyzer()	
#soup = scrape_start(url)
data=soup.find("div",{"id":"review-content"})
xyz=[]
for item in data.findAll("div",{"class":"review-block"}):
	dict={}
	dict['title']=item.find("h3").find(text=True).strip('\t\n')
	dict['date']=item.find("p",{"class":"review-author"}).find("span",{"class":"author-wrapper"}).find(text=True).strip('\t\n')
	dict['author']=item.find("p",{"class":"review-author"}).find("span",{"itemprop":"name"}).find(text=True).strip('\t\n')
	dict['comment']=item.find("p",{"class":"review-description"}).find(text=True).strip('\t\n')
	vs = analyzer.polarity_scores(dict['comment'])
	dict['sentiment'] = str(vs) 
	xyz.append(dict)
	#list_dict = xyz
#print(xyz)
con = pymysql.connect(user='root', password='pradeepika', database='customerreviews', charset='utf8')    
cursor = con.cursor()
DB_NAME = 'customerreviews'

for i in xyz:
	w = i['author'] 
	v = i['title']
	x = i['date']
	z = "\"" + i['comment'] + "\""
	u = i['sentiment'] 
	tl = [w,v,z,u]
	add_review = "INSERT INTO product_reviews(website_name, author, title, comment, sentiment) VALUES (%s, %s, %s, %s, %s)"
	cursor.execute(add_review, ("look_fantastic",tl[0],tl[1],tl[2],tl[3]))

cursor.close()

#def close_connection(cursor, con):
con.commit()
con.close()


