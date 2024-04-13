from flask import session
from database import db_session, Transakce
from core import dlouhe_datum, kratke_datum, uzivatel_list

def tr_new_device(input, poznamka):
    print("trigger.py | new_device() >>> spoušť při založení nového zařízení")
    x=uzivatel_list(session.get("uzivatel"))
    
    if input.zar_nakup != kratke_datum():
        actual_date = input.zar_nakup
    else:
        actual_date = kratke_datum()
    zalozeni = Transakce(tran_platnost_od=actual_date, tran_editace=dlouhe_datum(), tran_poznm = poznamka, id_uziv=x, id_zar=input.id_zar, id_lok=2, id_stat=1)
    db_session.add(zalozeni)
    db_session.commit()
    return zalozeni