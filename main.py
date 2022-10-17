import json

from flask import Flask
import sqlite3

app = Flask(__name__)

# Для корректного написания русских символов
app.config['JSON_AS_ASCII'] = False


@app.route("/movie/<title>")
def step_1(title):
	sqlite_query = f"""
					SELECT title, country, release_year, listed_in as genre, description FROM netflix
					WHERE title='{title}'
					ORDER BY date_added DESC
	"""

	result = None
	for item in run_sql(sqlite_query):
		result = dict(item)

	# return jsonify(result)
	# Для корректного написания русских символов и выставление красивой строки про помощи индент
	return app.response_class(json.dumps(result, ensure_ascii=False, indent=4), mimetype="application/json")


@app.route("/movie/<int:year1>/to/<int:year2>")
def step_2(year1, year2):
	sql = f"""
		SELECT title, release_year FROM netflix
		WHERE release_year BETWEEN {year1} AND {year2}
		ORDER BY release_year
		LIMIT 100
	"""

	result = []
	for item in run_sql(sql):
		result.append(dict(item))
	return app.response_class(json.dumps(result, ensure_ascii=False, indent=4), mimetype="application/json")


@app.route("/rating/<rating>")
def step_3(rating):
	my_dict = {
		"children": ("G", "G"),
		"family": ("G", "PG", "PG-13"),
		"adult": ("R", "NC-17")
	}

	sql = f"""
		select title, rating, description from netflix
		WHERE rating IN {my_dict.get(rating, ('PG-13', 'NC-17'))}
	"""

	result = []
	for item in run_sql(sql):
		result.append(dict(item))
	return app.response_class(json.dumps(result, ensure_ascii=False, indent=4), mimetype="application/json")


@app.route("/genre/<genre>")
def step_4(genre):
	sql = f"""
		select title, description from netflix
		WHERE listed_in LIKE '%{genre.title()}%'
		ORDER BY date_added DESC
		LIMIT 10
		"""

	result = []
	for item in run_sql(sql):
		result.append(dict(item))
	return app.response_class(json.dumps(result, ensure_ascii=False, indent=4), mimetype="application/json")


def step_5(name1='Rose McIver', name2='Ben Lamb'):
	sql = f"""
		select "cast" from netflix
		WHERE "cast" LIKE '%{name1}%' AND "cast" LIKE '%{name2}%'
	"""

	result = []
	for item in run_sql(sql):
		result.append(dict(item))

	main_name = {}
	for item in result:
		names = item.get('cast').split(", ")
		for name in names:
			# if name in main_name.keys():
			# 	main_name[name] += 1
			# else:
			# 	main_name[name] = 1

			# Альтернатива для строчек 92-95
			main_name[name] = main_name.get(name, 0) + 1


	# print(main_name)
	cast = []
	for item in main_name:
		if item not in (name1, name2) and main_name[item] > 2:
			cast.append(item)
	return cast


def step_6(types='Movie', year=2020, genre='Dramas'):
	sql = f"""
		SELECT title, description
		FROM netflix
		WHERE "type"='{types}'
		AND "release_year"='{year}'
		AND "listed_in" LIKE '%{genre}%'
	"""

	result = []
	for item in run_sql(sql):
		result.append(dict(item))
	# return result
	return json.dumps(result, indent=4, ensure_ascii=False)

def run_sql(sql):
	# with sqlite3.connect("./netflix.db") as connection:
	# 	return connection.cursor().execute(sql).fetchall()

	with sqlite3.connect("./netflix.db") as connection:
		connection.row_factory = sqlite3.Row

		return connection.execute(sql).fetchall()


# app.run(host="localhost", port=5000)

print(step_6())
