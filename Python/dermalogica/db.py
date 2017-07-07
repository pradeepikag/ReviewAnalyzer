import pymysql
import datetime
from vaderSentiment import SentimentIntensityAnalyzer

def insert_into_mysql(list_of_dict):
	cur, conn = create_conn_to_mysql()
	analyzer = SentimentIntensityAnalyzer()	
	for i in list_of_dict:
		a = ''
		b = ''
		xyz = i['name']
		try:
			a,b=xyz.split(',')
		except:
			a = xyz
		z = "\"" + i['comment'] + "\""
		s = date_error(i['date'])
		w = i['address']
		print(">>>>> returned date", s)
		#print(tpl[1])
		vs = analyzer.polarity_scores(i['comment'])
		#print(str(vs))
		sen = str(vs) 
		tpl = [xyz,z,s,sen]
		insert_into_table(cur, tpl)			
	close_connection(cur, conn) 

def create_conn_to_mysql():
	con = pymysql.connect(user='root', password='pradeepika', database='customerreviews', charset='utf8')    
	cursor = con.cursor()
	DB_NAME = 'customerreviews'
	return cursor, con

def date_error(s):
	formats = ['%b %d, %Y', '%b. %d, %Y', '%B %d, %Y']
	print("<<<< got date", s)
	try:
		for format_one in formats:
			try:
				return datetime.datetime.strptime(s, format_one).strftime('%Y-%m-%d')
			except ValueError:
				pass
	except:
		raise
	"""
	except ValueError:
		k = datetime.datetime.strptime(s, '%b. %d, %Y').strftime('%Y-%m-%d')
	finally:
		k = datetime.datetime.strptime(s, '%B %d, %Y').strftime('%Y-%m-%d')
	"""

def create_table():
	table = """CREATE TABLE reviews(
		name VARCHAR(100) PRIMARY KEY,
		content TEXT NOT NULL,
		date DATE NOT NULL,
		address VARCHAR(150))"""

def insert_into_table(cursor, tpl):
	add_review = "INSERT INTO product_reviews(website_name, author, comment, date, sentiment) VALUES (%s, %s, %s, %s, %s)"
	#print(tpl)
	cursor.execute(add_review, ("Consumer_Affairs",tpl[0],tpl[1],tpl[2],tpl[3]))

def date_conv():
	conv=time.strptime(from_date,"%a %b %d %Y")
	time.strftime("%Y-%m-%d",conv)

"""def senti(tpl):
	print(tpl[1])
	vs = analyzer.polarity_scores(tpl[1])
	print(str(vs))
	sen = str(vs)
	calc_senti= "INSERT INTO reviews(senti) VALUES (%s)"
	cursor.execute(calc_senti,sen)"""
	 

"""def get_table_content():
	query = ("SELECT * FROM reviews "
		"WHERE name='Benjamin of Goleta, CA'")"""

#cursor.execute(table)


#cursor.execute(query)


def close_connection(cursor, con):
	cursor.close()
	con.commit()
	con.close()
