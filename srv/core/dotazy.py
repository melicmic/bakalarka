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





                        print("sessions:")
        print(session.get("uzivatel",None))   
"""

from database import db_session

def serach_bar():
    db_session