from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, ShopScopedMixin, utcnow
from app.models.enums import PaymentMethod, SaleStatus


class Sale(ShopScopedMixin, BaseModel):
    __tablename__ = "sales"
    __table_args__ = (UniqueConstraint("shop_id", "client_ref", name="uq_sales_shop_client_ref"),)

    customer_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("customers.id"),
        nullable=True,
        index=True,
    )
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(16), nullable=False, default=PaymentMethod.CASH)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default=SaleStatus.COMPLETED)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
        server_default=func.now(),
        index=True,
    )
    client_ref: Mapped[str] = mapped_column(String(64), nullable=False)

    items: Mapped[list["SaleItem"]] = relationship(back_populates="sale")


class SaleItem(ShopScopedMixin, BaseModel):
    __tablename__ = "sale_items"

    sale_id: Mapped[str] = mapped_column(String(36), ForeignKey("sales.id"), nullable=False, index=True)
    product_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("products.id"),
        nullable=True,
        index=True,
    )
    name_snapshot: Mapped[str] = mapped_column(String(160), nullable=False)
    unit_price: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    line_total: Mapped[int] = mapped_column(Integer, nullable=False)

    sale: Mapped[Sale] = relationship(back_populates="items")
