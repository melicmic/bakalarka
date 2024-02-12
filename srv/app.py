from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from sqlalchemy import create_engine

#import core.vytvoreni_schema

import core.vytvoreni_schema 

app = Flask(__name__)

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/evihaw", future=True)

core.vytvoreni_schema.vytvoreni_ddl(engine)


@app.route('/')
def uvodni_stranka():
    print("ahoj")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
