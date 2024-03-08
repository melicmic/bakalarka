from sqlalchemy import select, and_

from database import db_session, Transakce, Zarizeni, Budova, Lokace

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