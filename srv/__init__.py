from flask import Flask
from flask import request, render_template, redirect, url_for, session

import psycopg2

from database import Uzivatel, Vyrobce, Zarizeni, Status, Kategorie, Budova, Lokace, Opravneni, Vztah, Transakce
from database import vytvoreni_ddl#, odkomentovat Base, engine
from database import naplneni_dat
from database import db_session

from views import login_bp, demo_bp, main_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'TAJNY_KLIC'

    vytvoreni_ddl()
    #Base.metadata.create_all(engine) # odkomentovat

    
    app.register_blueprint(main_bp, url_prefix="/signed")
    app.register_blueprint(login_bp, url_prefix="")
    app.register_blueprint(demo_bp, url_prefix="")
    return app

