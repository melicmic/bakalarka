"""        result = db_session.execute(select(Lokace, Budova).join(Lokace.fk_lok_bud)).first()
        
        #result = db_session.query(Lokace).join(Budova).filter(Budova.id_bud == 1)
        #print(result.id_lok)
        #print(result.lok_nazev)
        #print(result.bud_nazev)
        #print(result.fk_bud)
        print(result[1])

        stmt = select(Lokace, Budova).join(Lokace.fk_lok_bud).where(Lokace.fk_bud == 1).order_by(Lokace.lok_nazev)
        for row in db_session.execute(stmt):
                print(f"{row.Lokace.id_lok} {row.Budova.bud_nazev}")


        for row in y:
            print(f"{row.id_vyr} {row.vyr_nazev}")


                        print("sessions:")
        print(session.get("uzivatel",None))   
"""
from sqlalchemy.exc import DataError
from database import db_session, Zarizeni, Kategorie, Vyrobce, Uzivatel

def search_in_combo(text_pole, combo_pole):
    if combo_pole == 0:
        return Zarizeni.zar_inv == text_pole
    elif combo_pole == 1:
        return Zarizeni.zar_seriove == text_pole
    elif combo_pole == 2:
        return Zarizeni.zar_nazev == text_pole
    
def search_bar(text_pole, combo_pole):
    combo_pole = int(combo_pole)
    dotaz=None
    if combo_pole != 3:
        x = search_in_combo(text_pole, combo_pole)
        try:
            dotaz = db_session.query(Zarizeni).where(x).one_or_none()
        except DataError:
            print("v dotazech chybný datový formát")
            dotaz=False
            return dotaz

    elif combo_pole == 4:
        print("redireeect do uživatleů")
        x = Uzivatel.uziv_jmeno == text_pole
        dotaz = db_session.query(Uzivatel).where(x).one_or_none()
    else:
        print("redireeect do uživatleů")
        x = Uzivatel.uziv_kod == text_pole
        dotaz = db_session.query(Uzivatel).where(x).one_or_none()       
    return dotaz


def vyrobce_list():
    list_vyr = db_session.query(Vyrobce)
    return list_vyr

def kategorie_list():
    list_kat = db_session.query(Kategorie)
    return list_kat