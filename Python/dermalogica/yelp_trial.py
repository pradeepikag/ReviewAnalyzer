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

class Yelp(object):
	def start_scraping(self, searchterm):
		url = "https://www.yelp.com/search?find_loc=San+Francisco,+CA&find_desc="+searchterm
		url = "https://www.yelp.com/search?find_desc="+searchterm+"&find_loc=San+Francisco%2C+CA&ns=1"		
		list = []
		self.getReviews(url, list)
		print("****************************************************",len(list))
		return list		

	def getReviews(self, url, list):
		soup = get_drysoup(url)
		addr = self.getAddress(soup)
		res = soup.find(id="super-container")
		#=[]
for item in soup.findAll("div",{"class":"review review--with-sidebar"}):
	dict = {}
	#dict["user_name"] = item.find("div",{"class":"review-sidebar"}).find("div",{"class":"review-sidebar-content"}).find("div",{"class":"media-story"}).find("li",{"class":"user-name"}).find(text=True)					
	#dict["location"] = r.find("li",{"class":"user-location responsive-hidden-small"}).find(text=True)
	#dict["date"] = r.find("div",{"class":"review-content"}).find("span",{"rating-qualifier"}).find(text=True)
	dict["content"] = item.find("p",{"lang":"en"}).find(text=True)
	list.append(dict)
#print(list)
	print(list)
	return list

		"""if res is not None:		
			print(len(res.findAll("a",{"class":"biz-name-js-analytics-click"})))
			for item in res.findAll("a",{"class":"biz-name-js-analytics-click"}):
				d_url = item['href']
				detail = get_soup(d_url)
				reviews = detail.findAll("div",{"class":"review-list"})
				print(len(reviews))
				for r in reviews:
					dict = {}
					dict["user_name"] = r.find("li",{"class":"user-name"}).find(text=True)					
					dict["location"] = r.find("li",{"class":"user-location responsive-hidden-small"}).find(text=True)
					dict["date"] = r.find("div",{"class":"review-content"}).find("span",{"rating-qualifier"}).find(text=True)
					dict["content"] = r.find("div",{"class":"review-content"}).find('p').find(text=True, recursive=True)
					#dict["address"] = ""
					list.append(dict)
				break
			"""nextPage = self.getUrl(soup)
			if nextPage is not None:
				self.getReviews(nextPage, list)


	def getAddress(self, soup):
		try:
			return "\n".join(soup.find('div',{'class':'main-search_suggestions suggestions-list-container search-suggestions-list-container hidden'}).stripped_strings)
		except:
			return ""

#to get the url of next page
	
	def getUrl(self, soup):
		if soup.find("div",{"class":"review-list"}) is not None:
			print(getUrl)
			return "https://www.yelp.com/"+soup.find('a',{'class':'u-decoration-none next pagination-links_anchor'})['href']
		else:
			return None


