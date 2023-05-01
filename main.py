from utils import get_movie_by_title
from flask import Flask, Blueprint, render_template

app = Flask(__name__)


@app.route("/movie/<title>")
def movie_title(title):
    return get_movie_by_title(title)


app.run()
