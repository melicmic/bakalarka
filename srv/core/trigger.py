from flask import session
from database import db_session, Transakce
from core import dlouhe_datum, kratke_datum, uzivatel_list

def tr_new_device(input, popisek):
    print("trigger.py | new_device() >>> spoušť při založení nového zařízení")
    x=uzivatel_list(session.get("uzivatel"))
    print(x)
    zalozeni = Transakce(tran_platnost_od=kratke_datum(), tran_editace=dlouhe_datum(), tran_poznamka = popisek, fk_uziv=x, fk_zar=input.id_zar, fk_lok=2, fk_stat=1)
    db_session.add(zalozeni)
    db_session.commit()
    return zalozeni