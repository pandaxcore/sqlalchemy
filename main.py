import time
from sqlalchemy import select
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

LOGIN = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 5432
DB_NAME = "postgres"

engine = create_engine(
    f"postgresql+psycopg2://{LOGIN}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")


def add_data():
    with Session(engine) as session:
        spongebob = User(
            name="spongebob",
            fullname="Spongebob Squarepants",
            addresses=[Address(email_address="spongebob@sqlalchemy.org")]
        )
        sandy = User(
            name="sandy",
            fullname="Sandy Cheeks",
            addresses=[
                Address(email_address="sandy@sqlalchemy.org"),
                Address(email_address="sandy@squirrelpower.org"),
            ],
        )
        patrick = User(name="patrick", fullname="Patrick Star")
        session.add_all([spongebob, sandy, patrick])
        time.sleep(5)
        session.commit()


def get_data():
    pass


Base.metadata.create_all(engine)

if __name__ == "__main__":
    pass
