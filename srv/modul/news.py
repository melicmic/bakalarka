from flask import Blueprint, render_template, redirect, request, url_for, session
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from database import db_session, Zarizeni, Lokace, Budova, Transakce, Status, Uzivatel, Kategorie
from core import kratke_datum, vyrobce_list, kategorie_list, budovy_list, tr_new_device, my_role

news_bp = Blueprint("news", __name__)#, static_folder="static", template_folder="templates")

@news_bp.route("device", methods=["GET", "POST"])
def device():
    pravo = my_role()
    if pravo is True:
        print("má právo provádět změny")
        print("++ news.py | device() - vytvoření nového zařízení")
        if request.method == "POST":
            print("++ čtu vstupy z formuláře")
            input = Zarizeni(zar_inv = request.form["inv"],
                            zar_seriove = request.form["seriove"],
                            zar_model = request.form["model"] ,
                            zar_nakup = request.form["nakup"],
                            zar_poznm = request.form["poznm"] ,
                            fk_kat = request.form["kat"],
                            fk_vyr  = request.form["vyr"]                       
                            )
            db_session.add(input) 
            try:
                db_session.commit()
            except IntegrityError as e:
                print(f"chyba při vkládání {e}")
                db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
                return render_template("main/error.html", e=e)
            else:
                print("Zařízení založeno, trigger do transakce")
                id=input.zar_inv
                print(id)
                print(type(id))
                id_tr= tr_new_device(input).id_tran
                db_session.close()
                return redirect(url_for("news.transaction", id=id_tr))

        else:
            print("první načtení")
            y=vyrobce_list()
            k=kategorie_list()
            return render_template("news/device.html", x=kratke_datum(), y=y, k=k)

    else:
        return render_template("main/error.html", e="Nemáš právo na zapisování")


@news_bp.route("location", methods=["GET", "POST"])
def location():
    pravo = my_role()
    print("++ news.py | location() - vytvoření nového zařízení")
    if request.method == "POST":
        print("++ čtu vstupy z formuláře")
        input = Lokace(lok_kod = request.form["kod"].upper(),
                            lok_nazev = request.form["nazev"].upper(),
                            fk_bud = request.form["bud"]                   
                            )
        db_session.add(input) 

        try:
            db_session.commit()
        except IntegrityError as e:
            print(f"chyba při vkládání {e}")
            db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
            return render_template("error.html", e=e)
        except IntegrityError as e:
            print(f"chyba při vkládání {e}")
            db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
            return render_template("error.html", e=e)
        else:
            print("Zařízení založeno, trigger do transakce")

            db_session.close()
            return redirect(url_for("news.location"))

    else:
        print("první načtení")
        y=budovy_list()
        vypis = db_session.query(Lokace, Budova).join(Budova, Lokace.fk_bud == Budova.id_bud).order_by(Budova.bud_nazev).all()
        return render_template("news/location.html", y=y, x=vypis, pravo=pravo)


@news_bp.route("building", methods=["GET", "POST"])
def building():
    print("++ news.py | building() - vytvoření nového zařízení")
    pravo = my_role()
    if request.method == "POST":
        print("++ čtu vstupy z formuláře")
        input = Budova(bud_kod = request.form["kod"].upper(),
                bud_nazev = request.form["nazev"].upper(),   )               

        db_session.add(input) 
        try:
            db_session.commit()
        except IntegrityError as e:
            print(f"chyba při vkládání {e}")
            db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
            return render_template("error.html", e=e)
        else:
            print("Zařízení založeno, trigger do transakce")
            db_session.close()
            return redirect(url_for("news.building"))

    else:
        print("první načtení")
        y=budovy_list()
        
        return render_template("news/building.html", y=y, pravo=pravo)


@news_bp.route("manufacturer", methods=["GET", "POST"])
def manufacturer():
    pravo = my_role()
    print("++ news.py | manufacturer() - vytvoření nového zařízení")
    if request.method == "POST":
        print("++ čtu vstupy z formuláře")
        input = Zarizeni(zar_inv = request.form["inv"],
                         zar_nazev = request.form["nazev"],
                         zar_seriove = request.form["seriove"],
                         zar_model = request.form["model"] ,
                         zar_nakup = request.form["nakup"],
                         zar_poznm = request.form["poznm"] ,
                         fk_kat = request.form["kat"],
                         fk_vyr  = request.form["vyr"]                       
                         )
        db_session.add(input) 
        try:
            db_session.commit()
        except IntegrityError as e:
            print(f"chyba při vkládání {e}")
            db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
            return render_template("error.html", e=e)
        else:
            print("Zařízení založeno, trigger do transakce")
            db_session.close()
            return redirect(url_for("news.transaction"))

    else:
        print("první načtení")
        return render_template("news/manufacturer.html", pravo=pravo)

@news_bp.route("category", methods=["GET", "POST"])
def category():
    pravo = my_role()
    print("++ news.py | category() - vytvoření nového zařízení")
    if request.method == "POST":
        print("++ čtu vstupy z formuláře")
        input = Zarizeni(zar_inv = request.form["inv"],
                         zar_nazev = request.form["nazev"],
                         zar_seriove = request.form["seriove"],
                         zar_model = request.form["model"] ,
                         zar_nakup = request.form["nakup"],
                         zar_poznm = request.form["poznm"] ,
                         fk_kat = request.form["kat"],
                         fk_vyr  = request.form["vyr"]                       
                         )
        db_session.add(input) 
        try:
            db_session.commit()
        except IntegrityError as e:
            print(f"chyba při vkládání {e}")
            db_session.rollback() ##### nutnéééééééééééééééééééééééééééééééé
            return render_template("error.html", e=e)
        else:
            print("Zařízení založeno, trigger do transakce")
            db_session.close()
            return redirect(url_for("news.category"))

    else:
        print("první načtení")
        return render_template("news/category.html", pravo=pravo)


@news_bp.route("transaction", methods=["GET","POST"], defaults={"id": None})
@news_bp.route("transaction/<int:id>", methods=["GET","POST"])
def transaction(id):
    pravo = my_role()
    if id == None:
        print("id je none")
        print("první načtení")
        vypis= (db_session.query(Transakce, Zarizeni, Uzivatel, Lokace, Status, Kategorie)
                .join(Zarizeni, Transakce.fk_zar == Zarizeni.id_zar)
                .join(Uzivatel, Transakce.fk_uziv == Uzivatel.id_uziv)
                .join(Lokace, Transakce.fk_lok == Lokace.id_lok)
                .join(Status, Transakce.fk_stat == Status.id_stat)
                .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
                .order_by((Transakce.tran_editace))
                .limit(5).all()
                )
        return render_template("news/transaction.html", x=vypis, pravo=pravo)
    else:
        print(f"předané id je {id}")
        vypis= (db_session.query(Transakce, Zarizeni, Uzivatel, Lokace, Status, Kategorie)
                .join(Zarizeni, Transakce.fk_zar == Zarizeni.id_zar)
                .join(Uzivatel, Transakce.fk_uziv == Uzivatel.id_uziv)
                .join(Lokace, Transakce.fk_lok == Lokace.id_lok)
                .join(Status, Transakce.fk_stat == Status.id_stat)
                .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
                .where(Transakce.id_tran == id)).all()
        print("++ news.py | transaction() - zapsání transakce")
        return render_template("news/transaction.html", x=vypis, pravo=False)   
   


