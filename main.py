from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import insert


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/postgres"
)


def pg_connect():
    try:
        engine.connect()
        print("Connection established")
    except ConnectionError as error:
        print(error)


def migrate_tables():
    try:
        Base.metadata.create_all(engine)
    except ConnectionError as err:
        print(f"Migration were not transacted:{err}")


user_table = User


def insert_data():
    # stmt = insert(User).values(
    #     name="Patrick",
    #     fullname="Spongebob Squarepants"
    # )
    # compiled = stmt.compile()
    # print(compiled)
    stmt = insert(User).values([
        {"name": "sandy", "fullname": "Sandy Cheeks"},
        {"name": "patrick", "fullname": "Patrick Stars"},
    ])
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()


if __name__ == "__main__":
    pg_connect()
    migrate_tables()
    insert_data()
