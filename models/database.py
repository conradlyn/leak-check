from typing import List, Optional

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "source"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[Optional[str]]

    persons: Mapped[List["Person"]] = relationship(back_populates="source_obj")


class Person(Base):
    __tablename__ = "person"

    rowid: Mapped[int] = mapped_column(Integer, primary_key=True)

    id: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    receiver: Mapped[Optional[str]]
    nickname: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    address: Mapped[Optional[str]]
    car: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    qq: Mapped[Optional[int]]
    weibo: Mapped[Optional[int]]
    contact: Mapped[Optional[str]]
    company: Mapped[Optional[str]]
    source_id: Mapped[int] = mapped_column(ForeignKey("source.id"))

    # ORM 关系
    source_obj: Mapped["Source"] = relationship(back_populates="persons")