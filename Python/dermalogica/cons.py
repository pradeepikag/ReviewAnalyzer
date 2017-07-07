import requests
import dryscrape
from bs4 import BeautifulSoup
#from vaderSentiment import SentimentIntensityAnalyzer

def get_drysoup(url):
	print(url)
	session = dryscrape.Session()
	session.set_timeout(60)
	session.visit(url)
	page = session.body()
	soup = BeautifulSoup(page,'html.parser')
	return soup
def get_soup(url):
	print(url)
	page = requests.get(url)
	soup = BeautifulSoup(page.text,'html.parser')
	return soup

class ConsumerAffairs(object):
	def start_scraping(self, searchterm):
		url = "https://www.consumeraffairs.com/search.html?q="+searchterm
		list = []
		self.getReviews(url, list)
		print("****************************************************",len(list))
		return list		

	def getReviews(self, url, list):
		soup = get_drysoup(url)
		addr = self.getAddress(soup)
		res = soup.find(id="___gcse_0")
		#analyzer = SentimentIntensityAnalyzer()
		#for sentence in sentences:
    			#vs = analyzer.polarity_scores(sentence)
    			#print("{:-<65} {}".format(sentence, str(vs)))

		if res is not None:		
			print(len(res.findAll("a",{"class":"gs-title"})))
			for item in res.findAll("a",{"class":"gs-title"}):
				d_url = item['href']
				detail = get_soup(d_url)
				reviews = detail.findAll("div",{"class":"review--user-post"})
				#print(len(reviews))
				for r in reviews:
					dict = {}
					dict["name"] = r.find("span",{"class":"review__author-name"}).find(text=True)
					dict["date"] = r.find("span",{"class":"review__post-date"}).find(text=True)
					dict["comment"] = r.find("div",{"class":"review__body"}).find('p').find(text=True, recursive=True)
					dict["address"] = ""
					list.append(dict)
				break
			nextPage = self.getUrl(soup)
			if nextPage is not None:
				self.getReviews(nextPage, list)
			print(list)
			return list


	def getAddress(self, soup):
		try:
			return "\n".join(soup.find('div',{'itemprop':'address'}).stripped_strings)
		except:
			return ""

#to get the url of next page
	
	def getUrl(self, soup):
		if soup.find("div",{"class":"review--user-post"}) is not None:
			print(getUrl)
			return "https://www.consumeraffairs.com/"+soup.find('a',{'class':'next'})['href']
		else:
			return None
