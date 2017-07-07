from yelp_trial import *
name = input("Search for: ")

obj = Yelp()
obj.start_scraping(name)
