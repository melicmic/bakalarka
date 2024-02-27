import psycopg2

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .schema import Base

# Založení tabulek přes ORM
def vytvoreni_ddl():
    Base.metadata.create_all(engine)

# Nastavení připojení do db
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/evihaw", future=True)
print(f"connect.py | engine --|==|-- {engine.pool.status()}")
# Vytvoření objektu session pri přístup do db
Session = sessionmaker(bind=engine)
db_session = Session()