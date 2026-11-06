from enum import StrEnum


class PaymentMethod(StrEnum):
    CASH = "cash"
    MPESA = "mpesa"
    CREDIT = "credit"


class SaleStatus(StrEnum):
    COMPLETED = "completed"
    VOIDED = "voided"
    PENDING = "pending"


class MpesaStatus(StrEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
