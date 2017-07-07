import requests
import dryscrape
from bs4 import BeautifulSoup
import pymysql
from vaderSentiment import SentimentIntensityAnalyzer

url="http://www.dermalogica.co.uk/uk/html/products/daily-superfoliant-229.html"
session = dryscrape.Session()
session.set_timeout(60)
session.visit(url)
page = session.body()
soup = BeautifulSoup(page,'html.parser')
#return soup

#def scrape_in_dictformat():
analyzer = SentimentIntensityAnalyzer()	
#sam = scrape_start()
data =soup.find("div",{"class":"pr-contents-wrapper"})
xyz=[]
for item in data.findAll("div",{"class":"pr-review-wrap"}):
	dict={}
	dict['author']=item.find("p",{"class":"pr-review-author-name"}).find("span").find(text=True)
	dict['loc']=item.find("p",{"class":"pr-review-author-location"}).find("span").find(text=True)
	dict['title']=item.find("div",{"class":"pr-review-rating"}).find("p",{"class":"pr-review-rating-headline"}).find(text=True)
	dict['comment']=item.find("div",{"class":"pr-review-text"}).find("p",{"class":"pr-comments"}).find(text=True)
	#print(dict[comment],sen)		
	dict['age_grp']=(item.find("li",{"class":"pr-other-attribute-value"}).text)
	vs = analyzer.polarity_scores(dict['comment'])
	#print(str(vs))
	dict['sentiment'] = str(vs) 
	xyz.append(dict)
#return xyz;	
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
	tl = [v,w,x,z,u]
	add_review = "INSERT INTO product_reviews(website_name, author, loc, title, comment, sentiment) VALUES(%s, %s, %s, %s, %s, %s)"
	cursor.execute(add_review, ("dermalogica",tl[0],tl[1],tl[2],tl[3],tl[4]))

cursor.close()

#def close_connection(cursor, con):
con.commit()
con.close()


