from database import db_session, Transakce
from core import dlouhe_datum

def tr_new_device(input):
    print("trigger.py | new_device() >>> spoušť při založení nového zařízení")
    zalozeni = Transakce(tran_platnost_od=dlouhe_datum(), tran_editace=dlouhe_datum(), tran_poznamka = "Naskladnění", fk_uziv=4, fk_zar=input.id_zar, fk_lok=1, fk_stat=12,)
    db_session.add(zalozeni)
    db_session.commit()
    return zalozeni