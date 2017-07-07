import pymysql as sql
import pandas as pd

db_connection = sql.connect(database='customerreviews', user='root', password='pradeepika', charset='utf8')
#db_cursor = db_connection.cursor()
#db_cursor.execute('SELECT * FROM table_name')

#table_rows = db_cursor.fetchall()

#df = pd.DataFrame(table_rows)

df = pd.read_sql('SELECT * FROM reviews', con=db_connection)
print(df)
