from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey

from typing import List, Optional
import datetime

# Párování SQL na ORM-Python
class Base(DeclarativeBase):
    pass

# Definice tabulek v DB
class Vyrobce(Base):
    __tablename__ = "Vyrobci_tab"
    id_vyr: Mapped[int] = mapped_column(primary_key=True)
    vyr_nazev: Mapped[str] = mapped_column(String(30)) # název výrobce
    
    fk_vyr_zar: Mapped[List["Zarizeni"]] = relationship(back_populates="fk_zar_vyr")

    def __repr__(self) -> str:
        return f"Vyrobce(id={self.id_vyr!r}, name={self.vyr_nazev!r})"

class Kategorie(Base):
    __tablename__ = "Kategorie_tab"
    id_kat: Mapped[int] = mapped_column(primary_key=True)
    kat_nazev: Mapped[str] = mapped_column(String(30)) # název kategorie - pc, ntbk, workst,...

    fk_kat_zar: Mapped[List["Zarizeni"]] = relationship(back_populates="fk_zar_kat")

class Status(Base):
    __tablename__ = "Statusy_tab"
    id_stat: Mapped[int] = mapped_column(primary_key=True)
    stat_nazev: Mapped[str] = mapped_column(String(30)) # název statusu

    fk_stat_tran: Mapped[List["Transakce"]] = relationship(back_populates="fk_tran_stat")

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
    fk_kat: Mapped[int] = mapped_column(ForeignKey("Kategorie_tab.id_kat"))
    fk_vyr: Mapped[int] = mapped_column(ForeignKey("Vyrobci_tab.id_vyr"))
    
    fk_zar_tran: Mapped[List["Transakce"]] = relationship(back_populates="fk_tran_zar")
    fk_zar_vyr: Mapped[List["Vyrobce"]] = relationship(back_populates="fk_vyr_zar")
    fk_zar_kat: Mapped[List["Kategorie"]] = relationship(back_populates="fk_kat_zar")

class Uzivatel(Base):
    __tablename__ = "Uzivatele_tab"
    id_uziv: Mapped[int] = mapped_column(primary_key=True)
    uziv_kod: Mapped[str] = mapped_column(String(30)) # id-čko
    uziv_jmeno: Mapped[str] = mapped_column(String(30)) # jméno
    uziv_prijemni: Mapped[str] = mapped_column(String(30)) # příjmené
    uziv_email: Mapped[str] = mapped_column(String(30)) # email
    uziv_nastup: Mapped[datetime.date] = mapped_column(Date) # den nástupu
    uziv_vystup: Mapped[datetime.date] = mapped_column(Date) # den ukončení
    uziv_heslo: Mapped[str] = mapped_column(String(30)) # heslo
    # FK - vztah, opravneni
    fk_vzt: Mapped[int] = mapped_column(ForeignKey("Vztahy_tab.id_vzt"))
    fk_opr: Mapped[int] = mapped_column(ForeignKey("Opravneni_tab.id_opr"))
    
    fk_uziv_tran: Mapped[List["Transakce"]] = relationship(back_populates="fk_tran_uziv")
    fk_uziv_opr: Mapped[List["Opravneni"]] = relationship(back_populates="fk_opr_uziv")
    fk_uziv_vzt: Mapped[List["Vztah"]] = relationship(back_populates="fk_vzt_uziv")

class Vztah(Base):
    __tablename__ = "Vztahy_tab"
    id_vzt: Mapped[int] = mapped_column(primary_key=True)
    vzt_nazev: Mapped[str] = mapped_column(String(30)) # název vztahu - externi, interni, vyrobni, ot

    fk_vzt_uziv: Mapped[List["Uzivatel"]] = relationship(back_populates="fk_uziv_vzt")

class Opravneni(Base):
    __tablename__ = "Opravneni_tab"
    id_opr: Mapped[int] = mapped_column(primary_key=True)
    opr_nazev: Mapped[str] = mapped_column(String(30)) # název oprávnění
    
    fk_opr_uziv: Mapped[List["Uzivatel"]] = relationship(back_populates="fk_uziv_opr")
    # admin, čtení, zadny

class Lokace(Base):
    __tablename__ = "Lokace_tab"
    id_lok: Mapped[int] = mapped_column(primary_key=True)
    lok_kod: Mapped[str] = mapped_column(String(30)) # kód lokace
    lok_nazev: Mapped[str] = mapped_column(String(30)) # název lokace

    fk_bud: Mapped[int] = mapped_column(ForeignKey("Budovy_tab.id_bud"))

    fk_lok_tran: Mapped[List["Transakce"]] = relationship(back_populates="fk_tran_lok")
    fk_lok_bud: Mapped[List["Budova"]] = relationship(back_populates="fk_bud_lok")

class Budova(Base):
    __tablename__ = "Budovy_tab"
    id_bud: Mapped[int] = mapped_column(primary_key=True)
    bud_nazev: Mapped[str] = mapped_column(String(30)) # název budovy A-B-C

    fk_bud_lok: Mapped[List["Lokace"]] = relationship(back_populates="fk_lok_bud")

class Transakce(Base):
    __tablename__ = "Transakce_tab"
    id_tran: Mapped[int] = mapped_column(primary_key=True)
    tran_platnost_od: Mapped[datetime.datetime] = mapped_column(Date) # název oprávnění
    tran_platnost_do: Mapped[datetime.datetime] = mapped_column(Date) # popis oprávnění  
    tran_poznamka: Mapped[str] = mapped_column(String(30)) # poznámka oprávnění
    tran_editace: Mapped[datetime.datetime] = mapped_column(Date)

    fk_uziv: Mapped[int] = mapped_column(ForeignKey("Uzivatele_tab.id_uziv"))
    fk_zar: Mapped[int] = mapped_column(ForeignKey("Zarizeni_tab.id_zar"))
    fk_lok: Mapped[int] = mapped_column(ForeignKey("Lokace_tab.id_lok"))
    fk_stat: Mapped[int] = mapped_column(ForeignKey("Statusy_tab.id_stat"))

    fk_tran_uziv: Mapped[List["Uzivatel"]] = relationship(back_populates="fk_uziv_tran")
    fk_tran_zar: Mapped[List["Zarizeni"]] = relationship(back_populates="fk_zar_tran")
    fk_tran_lok: Mapped[List["Lokace"]] = relationship(back_populates="fk_lok_tran")
    fk_tran_stat: Mapped[List["Status"]] = relationship(back_populates="fk_stat_tran")
    # FK - zamestanenc, zarizeni, lokace, status, 

