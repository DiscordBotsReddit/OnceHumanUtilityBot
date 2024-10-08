from typing import List
from sqlalchemy import BigInteger, Integer, Boolean, ForeignKey # type: ignore
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column # type: ignore

class Base(DeclarativeBase):
    pass

class CrateRespawnChannel(Base):
    __tablename__ = "craterespawn_channels"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    channel_id: Mapped[int] = mapped_column(BigInteger)
    role_id: Mapped[int] = mapped_column(BigInteger, default=None)
    added_by: Mapped[int] = mapped_column(BigInteger)

class CargoScrambleChannel(Base):
    __tablename__ = "cargoscramble_channels"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    channel_id: Mapped[int] = mapped_column(BigInteger)
    role_id: Mapped[int] = mapped_column(BigInteger, default=None)
    added_by: Mapped[int] = mapped_column(BigInteger)

class CrateMutes(Base):
    __tablename__ = "crate_mutes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('craterespawn_channels.guild_id'))
    zero: Mapped[bool] = mapped_column(Boolean)
    four: Mapped[bool] = mapped_column(Boolean)
    eight: Mapped[bool] = mapped_column(Boolean)
    twelve: Mapped[bool] = mapped_column(Boolean)
    sixteen: Mapped[bool] = mapped_column(Boolean)
    twenty: Mapped[bool] = mapped_column(Boolean)

class CargoMutes(Base):
    __tablename__ = "cargo_mutes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('cargoscramble_channels.guild_id'))
    twelve: Mapped[bool] = mapped_column(Boolean)
    fifteen: Mapped[bool] = mapped_column(Boolean)
    twenty_two: Mapped[bool] = mapped_column(Boolean)
    eighteen_thirty: Mapped[bool] = mapped_column(Boolean)