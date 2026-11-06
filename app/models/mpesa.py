from sqlalchemy import ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel, ShopScopedMixin
from app.models.enums import MpesaStatus


class MpesaPayment(ShopScopedMixin, BaseModel):
    __tablename__ = "mpesa_payments"

    sale_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("sales.id"),
        nullable=True,
        index=True,
    )
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    mpesa_receipt: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default=MpesaStatus.PENDING)
    raw_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
