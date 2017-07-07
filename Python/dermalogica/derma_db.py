import pymysql
from dermapro import *

def insert_into_mysql():
	cur, conn = create_conn_to_mysql()
	hhh = scrape_in_dictformat()	
	#print(list_dict)	
	for i in hhh:
		w = i['author']
		x = i['title']
		y = i['loc']
		z = "\"" + i['comment'] + "\""
		v = i['age_grp']
		#vs = analyzer.polarity_scores(i['comment'])
		#print(str(vs))
		sen = str(vs) 
		tl = [w,x,y,z,v]
		insert_into_table(cur, tl)		
	close_connection(cur, conn) 

def create_conn_to_mysql():
	con = pymysql.connect(user='root', password='pradeepika', database='dermarev', charset='utf8')    
	cursor = con.cursor()
	DB_NAME = 'dermarev'
	return cursor, con

def insert_into_table(cursor, t_list):
	#insert_into_mysql(lst)
	add_review = "INSERT INTO dermareviews(author, title, loc, comment, age) VALUES (%s, %s, %s, %s, %s)"
	cursor.execute(add_review, (t_list[0],t_list[1],t_list[2],t_list[3],t_list[4]))

#def get_table_content():
	#query = ("SELECT * FROM dermareviews WHERE name='Happy D'")

def close_cursor(cursor):
	cursor.close()

def close_connection(cursor, con):
	con.commit()
	con.close()
