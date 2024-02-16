from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from sqlalchemy import create_engine

from core import vytvoreni_schema, demo_data

app = Flask(__name__)

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/evihaw", future=True)

vytvoreni_schema.vytvoreni_ddl(engine)


@app.route('/')
def uvodni_stranka():
    print("ahoj")
    return render_template("index.html")

@app.route("/demo_data")
def demo_lokace():
    print("vložení statických dat")
    demo_data.naplneni_dat(engine)



if __name__ == "__main__":
    app.run(debug=True)
