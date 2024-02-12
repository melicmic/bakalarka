import datetime
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey

class Base(DeclarativeBase):
    pass
  
class Vyrobce(Base):
    __tablename__ = "Vyrobci_tab"
    id_vyr: Mapped[int] = mapped_column(primary_key=True)
    vyr_nazev: Mapped[str] = mapped_column(String(30)) # název výrobce
    
    fk_vyr_zar: Mapped[List["Zarizeni"]] = relationship()

    def __repr__(self) -> str:
        return f"Vyrobce(id={self.id_vyr!r}, name={self.vyr_nazev!r})"

class Kategorie(Base):
    __tablename__ = "Kategorie_tab"
    id_kat: Mapped[int] = mapped_column(primary_key=True)
    kat_nazev: Mapped[str] = mapped_column(String(30)) # název kategorie - pc, ntbk, workst,...

    fk_kat_zar: Mapped[List["Zarizeni"]] = relationship()

class Status(Base):
    __tablename__ = "Statusy_tab"
    id_stat: Mapped[int] = mapped_column(primary_key=True)
    stat_nazev: Mapped[str] = mapped_column(String(30)) # název statusu

    fk_stat_zar: Mapped[List["Zarizeni"]] = relationship()

    fk_stat_tran: Mapped[List["Transakce"]] = relationship()

class Zarizeni(Base):
    __tablename__ = "Zarizeni_tab"
    id_zar: Mapped[int] = mapped_column(primary_key=True)
    zar_inv: Mapped[int] = mapped_column(Integer) # inventární číslo
    zar_nazev: Mapped[str] = mapped_column(String(30)) # domenové jméno
    zar_seriove: Mapped[str] = mapped_column(String(30)) # sériové číslo
    zar_model: Mapped[str] = mapped_column(String(30)) # model zařízení
    zar_nakup: Mapped[datetime.date] = mapped_column(Date) # datum nakupu
    zar_poznm: Mapped[str] = mapped_column(String(64)) # poznámka
    # FK - kategorie, model->výrobce?, status?
    fk_zar_kat: Mapped[int] = mapped_column(ForeignKey("Kategorie_tab.id_kat"))
    fk_zar_vyr: Mapped[int] = mapped_column(ForeignKey("Vyrobci_tab.id_vyr"))
    fk_zar_stat: Mapped[int] = mapped_column(ForeignKey("Statusy_tab.id_stat"))

    fk_zar_tran: Mapped[List["Transakce"]] = relationship()


class Uzivatele(Base):
    __tablename__ = "Uzivatele_tab"
    id_uziv: Mapped[int] = mapped_column(primary_key=True)
    uziv_kod: Mapped[str] = mapped_column(String(30)) # id-čko
    uziv_jmeno: Mapped[str] = mapped_column(String(30)) # jméno
    uziv_prijemni: Mapped[str] = mapped_column(String(30)) # příjmené
    uziv_email: Mapped[str] = mapped_column(String(30)) # email
    uziv_start: Mapped[str] = mapped_column(String(30)) # den nástupu
    uziv_konec: Mapped[str] = mapped_column(String(30)) # den ukončení
    uziv_heslo: Mapped[str] = mapped_column(String(30)) # heslo
    # FK - vztah, opravneni
    fk_uziv_vzt: Mapped[int] = mapped_column(ForeignKey("Vztahy_tab.id_vzt"))
    fk_uziv_opr: Mapped[int] = mapped_column(ForeignKey("Opravneni_tab.id_opr"))
    
    fk_uziv_tran: Mapped[List["Transakce"]] = relationship()

class Vztah(Base):
    __tablename__ = "Vztahy_tab"
    id_vzt: Mapped[int] = mapped_column(primary_key=True)
    vzt_nazev: Mapped[str] = mapped_column(String(30)) # název vztahu - externi, interni, vyrobni, ot

    fk_vzt_uziv: Mapped[List["Uzivatele"]] = relationship()

class Opravneni(Base):
    __tablename__ = "Opravneni_tab"
    id_opr: Mapped[int] = mapped_column(primary_key=True)
    opr_nazev: Mapped[str] = mapped_column(String(30)) # názzev oprávnění
    opr_popis: Mapped[str] = mapped_column(String(30)) # popis oprávnění  
    
    fk_opr_uziv: Mapped[List["Uzivatele"]] = relationship()
    # admin, čtení, zadny

class Lokace(Base):
    __tablename__ = "Lokace_tab"
    id_lok: Mapped[int] = mapped_column(primary_key=True)
    lok_kod: Mapped[str] = mapped_column(String(30)) # kód lokace
    lok_nazev: Mapped[str] = mapped_column(String(30)) # název lokace

    fk_lok_bud: Mapped[int] = mapped_column(ForeignKey("Budovy_tab.id_bud"))

    fk_lok_tran: Mapped[List["Transakce"]] = relationship()

class Budova(Base):
    __tablename__ = "Budovy_tab"
    id_bud: Mapped[int] = mapped_column(primary_key=True)
    bud_nazev: Mapped[str] = mapped_column(String(30)) # název budovy A-B-C

    fk_bud_lok: Mapped[List["Lokace"]] = relationship()

class Transakce(Base):
    __tablename__ = "Transakce_tab"
    id_tran: Mapped[int] = mapped_column(primary_key=True)
    tran_platnost_od: Mapped[str] = mapped_column(String(30)) # název oprávnění
    tran_platnost_do: Mapped[str] = mapped_column(String(30)) # popis oprávnění  
    tran_poznamka: Mapped[str] = mapped_column(String(30)) # poznámka oprávnění

    fk_tran_uziv: Mapped[int] = mapped_column(ForeignKey("Uzivatele_tab.id_uziv"))
    fk_tran_zar: Mapped[int] = mapped_column(ForeignKey("Zarizeni_tab.id_zar"))
    fk_tran_lok: Mapped[int] = mapped_column(ForeignKey("Lokace_tab.id_lok"))
    fk_tran_stat: Mapped[int] = mapped_column(ForeignKey("Statusy_tab.id_stat"))

    # FK - zamestanenc, zarizeni, lokace, status, 







def vytvoreni_ddl(engine):
    Base.metadata.create_all(engine)