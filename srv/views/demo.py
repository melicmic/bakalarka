# demo page, naplní data z prohlížeče
from flask import Blueprint
from database import naplneni_dat

demo_bp = Blueprint("demo", __name__)

@demo_bp.route("/demo_data")
def demo_data():
        print("vložení statických dat")
        naplneni_dat()
        return "<h1>Naplnění demo dat</h1>"