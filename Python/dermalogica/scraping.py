from cons import *
from db import * #this is the one with db integration
name = input("Enter a Business: ")

obj = ConsumerAffairs()
lst = obj.start_scraping(name)
insert_into_mysql(lst)
