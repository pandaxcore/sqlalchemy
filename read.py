import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import mapped_column
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
COLUMN_MAP = {
    "First Name": "first_name",
    "Last Name": "last_name",
    "Gender": "gender",
    "Country": "country",
    "Age": "age",
    "Date": "date",
    "Id": "tab_num"
}


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(10))
    country: Mapped[Optional[str]] = mapped_column(String(50))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    date: Mapped[Optional[str]] = mapped_column(Date)
    tab_num: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False)


engine = create_engine(URL)
Base.metadata.create_all(engine)

df = pd.read_excel('file_example_XLS_10.xls')\

with Session(engine) as session:
    for _, row in df.iterrows():
        person = Person(
            first_name=row["First Name"],
            last_name=row["Last Name"],
            gender=row["Gender"],
            country=row["Country"],
            age=int(row["Age"]),
            date=datetime.strptime(row["Date"], "%d/%m/%Y").date(),
            tab_num=int(row["Id"]),
        )
        print(person)
        session.add(person)
    session.commit()
    session.close()
