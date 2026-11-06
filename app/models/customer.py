from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel, ShopScopedMixin


class Customer(ShopScopedMixin, BaseModel):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(160), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
