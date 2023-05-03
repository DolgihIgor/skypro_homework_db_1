import sqlite3

from flask import Flask, Blueprint, render_template, jsonify


def db_connect(query):
    connections = sqlite3.connect('netflix.db')
    cursor = connections.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connections.close()
    return result


def main():

    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = True
    app.config['DEBUG'] = True

    @app.route("/")
    def main_page():
        return "Это главная страница сайта!"

    # 1. Поиск фильма в БД по названию
    @app.route("/movie/<title>")
    def search_by_title(title):
        query = f"""
            SELECT
                 title
                 , country 
                 , release_year
                 , listed_in AS genre
                 , description
             FROM netflix
             WHERE title = '{title}'
             ORDER BY release_year DESC
             LIMIT 1  
        """
        response = db_connect(query)[0]
        response_json = {
            'title': response[0],
            'country': response[1],
            'release_year': response[2],
            'genre': response[3],
            'description': response[4].strip(),  # Убираем перенос строки в конце
        }
        return jsonify(response_json)

    # 2. Поиск фильма в БД по году выхода от и до
    @app.route("/movie/<int:start>/to/<int:end>")
    def movies_range_of_years(start, end):
        query = f"""
        SELECT
            title
            , release_year
        FROM netflix
        WHERE release_year BETWEEN {start} AND {end}
        ORDER BY release_year
        LIMIT 100
"""
        response = db_connect(query)
        response_json = []

        for film in response:
            response_json.append({
                'title': film[0],
                'release_year': film[1],
            })
        return jsonify(response_json)

    # 3. Поиск фильма в БД по рейтингу
    @app.route('/rating/<group>')
    def search_by_rating(group):
        levels = {
            'children': ['G'],
            'family': ['G', 'PG', 'PG-13'],
            'adult': ['R', 'NC-17']
        }

        if group in levels:
            level = '\", \"'.join(levels[group])
            level = f'\"{level}\"'
        else:
            return jsonify([])

        query = f"""
            SELECT
                title
                , rating
                , description
            FROM netflix
            WHERE rating IN ({level})
        """
        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'rating': film[1],
                'description': film[2]
            })
        return jsonify(response_json)

    # 4. Поиск фильма в БД по жанру
    @app.route('/genre/<genre>')
    def search_by_genre(genre):
        query = f"""
            SELECT
                title
                , release_year
                , listed_in AS genre
                , description
            FROM netflix
            WHERE genre LIKE ("%{genre}%")
            ORDER BY release_year DESC
            LIMIT 10
        """
        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'genre': film[2],
                'description': film[3]
            })
        return jsonify(response_json)

    def get_actors(name1, name2):
        query = f"""
        SELECT
            "cast"
        FROM netflix
        WHERE "cast" LIKE '%{name1}%'
            AND "cast" LIKE '%{name2}%'        
        """

        response = db_connect(query)
        actors = []
        for cast in response:
            actors.extend(cast[0].split(', '))
        result = []
        for a in actors:
            if a not in [name1, name2]:
                if actors.count(a) > 2:
                    result.append(a)
        result = set(result)  # добавим во множество, чтобы исключить повторения

        print(result)

    def get_films(type_film, release_year, genre):
        query = f"""
            SELECT
                title
                , description
            FROM netflix
            WHERE "type" = '{type_film}'
                AND release_year = {release_year}
                AND listed_in LIKE '%{genre}%'
        """

        response = db_connect(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'description': film[1]
            })
        for film in response_json:
            print(film)

    # get_films('Movie', '2016', 'Dramas')
    # get_actors('Rose McIver', 'Ben Lamb')
    # app.run()


if __name__ == '__main__':
    main()
