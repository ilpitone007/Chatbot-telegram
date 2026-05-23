from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, JSON
from datetime import datetime
from typing import Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True) # UUID interno
    lang: Mapped[Optional[str]] = mapped_column(String)
    gender: Mapped[Optional[str]] = mapped_column(String)
    display_name: Mapped[Optional[str]] = mapped_column(String)
    age_range: Mapped[Optional[str]] = mapped_column(String)
    hobbies: Mapped[Optional[list[str]]] = mapped_column(JSON)
    level: Mapped[str] = mapped_column(String, default="newbie")
    total_points: Mapped[int] = mapped_column(Integer, default=0)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    suspended_until: Mapped[Optional[datetime]] = mapped_column(DateTime)
    warning_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_active_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_a_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user_b_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    end_reason: Mapped[Optional[str]] = mapped_column(String)
    rating_a: Mapped[Optional[int]] = mapped_column(Integer)
    rating_b: Mapped[Optional[int]] = mapped_column(Integer)
    message_count: Mapped[int] = mapped_column(Integer, default=0)

class Referral(Base):
    __tablename__ = "referrals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    referrer_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    referred_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    level: Mapped[int] = mapped_column(Integer) # 1 o 2
    link_token: Mapped[str] = mapped_column(String)
    link_expires_at: Mapped[datetime] = mapped_column(DateTime)
    bonus_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class PointsLog(Base):
    __tablename__ = "points_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(String)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reporter_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    reported_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    session_hash: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Blacklist(Base):
    __tablename__ = "blacklist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String, unique=True)
    severity: Mapped[str] = mapped_column(String) # warn o block
    added_by: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
