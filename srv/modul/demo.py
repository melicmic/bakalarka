# demo page, naplní data z prohlížeče
from flask import Blueprint, render_template
from database import naplneni_dat

demo_bp = Blueprint("demo", __name__)

@demo_bp.route("/demo_data")
def demo_data():
        print("vložení statických dat")
        naplneni_dat()
        return render_template("main/error.html", e="Naplnění demo dat")