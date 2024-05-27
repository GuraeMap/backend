from sqlalchemy import BigInteger, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.db.time_stamp_mixin import TimeStampMixin
from app.api.v1.user.entity.user import User


class Product(TimeStampMixin):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(255))
    selling_price: Mapped[int] = mapped_column(Integer, doc="판매 가격")
    cost_price: Mapped[int] = mapped_column(Integer, doc="원가")
    name: Mapped[str] = mapped_column(String(255), doc="상품명")
    description: Mapped[str] = mapped_column(String(255), doc="상품 설명")
    barcode: Mapped[str] = mapped_column(String(255), doc="바코드")
    expiration_date: Mapped[DateTime] = mapped_column(DateTime, doc="유통기한")
    size: Mapped[str] = mapped_column(String(255), doc="사이즈")
    search_keywords: Mapped[str] = mapped_column(Text, index=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))

    user = relationship("User")
