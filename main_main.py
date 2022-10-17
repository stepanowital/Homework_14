import sqlite3


def run_sql(sql):
	with sqlite3.connect("./netflix.db") as connection:
		connection.row_factory = sqlite3.Row

		return connection.execute(sql).fetchall()


sql = "select * from netflix"

for item in run_sql(sql):
	print(dict(item))
