from sqlalchemy import String, Boolean, Integer

from app.config.db.time_stamp_mixin import TimeStampMixin
from sqlalchemy.orm import mapped_column, Mapped


class User(TimeStampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_phone: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    is_session: Mapped[bool] = mapped_column(Boolean, default=0, doc="1 : 회원 탈퇴 ")
