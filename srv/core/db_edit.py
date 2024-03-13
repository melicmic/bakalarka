from sqlalchemy import select, update, insert, and_

from core import dlouhe_datum, kratke_datum
from database import db_session, Transakce, Zarizeni, Budova, Lokace, Kategorie, Vyrobce, Opravneni, Vztah, Uzivatel

def edit_list(id_list):
    results = []
    for id in id_list:
        stmt = (select(Transakce, Zarizeni, Lokace, Budova)
                .join(Zarizeni, Transakce.fk_zar == Zarizeni.id_zar)
                .join(Lokace, Transakce.fk_lok == Lokace.id_lok)
                .join(Budova, Lokace.fk_bud == Budova.id_bud)
                .where(and_(Zarizeni.zar_inv == int(id), Transakce.tran_platnost_do == None)))
        result = db_session.execute(stmt).all()
        results.append(result)
    return results

def write_change(id, lok, status, date, popis, user, zar):
        print("jsem uvnitr")
        with db_session as ssn:
              with ssn.begin():
                        update_stmt = (update(Transakce).where((Transakce.id_tran == id) & (Transakce.tran_platnost_do == None))
                                .values(
                                tran_platnost_do=date,
                                tran_editace=dlouhe_datum()
                        ))
                        ssn.execute(update_stmt)
                        insert_stmt = (insert(Transakce).values(tran_platnost_od=kratke_datum(), tran_editace=dlouhe_datum(), 
                                                                tran_poznamka = popis, fk_uziv=user, fk_zar=zar, fk_lok=lok, fk_stat=status))
                        
                        ssn.execute(insert_stmt)


# Tabulka Zarízení_tab pro úpravu zakladních parametrů.
def load_device(id):
    print(id)
    stmt = (select(Zarizeni, Kategorie, Vyrobce)
                .join(Kategorie, Zarizeni.fk_kat == Kategorie.id_kat)
                .join(Vyrobce, Zarizeni.fk_vyr == Vyrobce.id_vyr)
                .where(Zarizeni.id_zar == id))
    result = db_session.execute(stmt).first()
    return result

# Tabulka Zařízení_tab: aktualizace dat k úpravě
def db_update_device(id, new_seriove, new_model, new_info, new_kat, new_vyr):
    with db_session as ssn:
        with ssn.begin():
            update_stmt = (update(Zarizeni).where(Zarizeni.id_zar == id)
                    .values(
                    zar_seriove = new_seriove,
                    zar_model = new_model,
                    zar_poznm = new_info,
                    fk_kat = new_kat,
                    fk_vyr = new_vyr
            ))
            ssn.execute(update_stmt)


def load_user(id):
    stmt = (select(Uzivatel, Vztah, Opravneni)
                .join(Vztah, Uzivatel.fk_vzt == Vztah.id_vzt)
                .join(Opravneni, Uzivatel.fk_opr == Opravneni.id_opr)
                .where(Uzivatel.id_uziv == id))
    result = db_session.execute(stmt).first()
    return result


def db_update_user(id, new_jmeno, new_prijmeni, new_vzt, new_opr, new_heslo, new_email):
    with db_session as ssn:
        with ssn.begin():
            update_stmt = (update(Uzivatel).where(Uzivatel.id_uziv == id)
                    .values(
                    uziv_jmeno = new_jmeno,
                    uziv_prijmeni = new_prijmeni,
                    fk_vzt = new_vzt,
                    fk_opr = new_opr,
                    uziv_heslo = new_heslo,
                    uziv_email = new_email
            ))
            ssn.execute(update_stmt)

def db_discard_user(id, new_vystup):
         with db_session as ssn:
            with ssn.begin():
                update_stmt = (update(Uzivatel).where(Uzivatel.id_uziv == id)
                        .values(
                        uziv_vystup = new_vystup
                ))
                ssn.execute(update_stmt)