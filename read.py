from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer
from datetime import date
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import Session


class Base(DeclarativeBase):
    pass


class People(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(7))
    country: Mapped[str] = mapped_column(String(50))
    age: Mapped[int]
    date: Mapped[date]
    tab_num: Mapped[int] = mapped_column(Integer())


engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")

Base.metadata.create_all(engine)

excel = pd.read_excel("file_example_XLS_10.xlsx")

excel["Date"] = pd.to_datetime(excel["Date"], dayfirst=True)
excel["Country"] = excel["Country"].fillna("UNKNOWN")

session = Session(engine)

for index, row in excel.iterrows():
    rows = People(
        first_name=row["First Name"],
        last_name=row["Last Name"],
        gender=row["Gender"],
        country=row["Country"],
        age=row["Age"],
        date=row["Date"],
        tab_num=row["Id"]
    )
    session.add(rows)

session.commit()
session.close()
