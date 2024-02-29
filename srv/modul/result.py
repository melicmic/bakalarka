from flask import Blueprint, render_template, redirect, request, url_for, session

from database import db_session, Zarizeni, Kategorie
from core import kratke_datum, vyrobce_list, kategorie_list

result_bp = Blueprint("result", __name__)