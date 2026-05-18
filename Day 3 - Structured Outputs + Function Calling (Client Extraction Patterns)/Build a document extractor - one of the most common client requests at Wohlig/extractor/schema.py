from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


# ====================================
# ENUM
# ====================================

class InvoiceStatus(str, Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"
    OVERDUE = "OVERDUE"


# ====================================
# NESTED OBJECT
# ====================================

class VendorAddress(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str


# ====================================
# LINE ITEM
# ====================================

class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    line_total: float


# ====================================
# MAIN MODEL
# ====================================

class InvoiceExtraction(BaseModel):

    invoice_number: str

    invoice_date: str

    vendor_name: str

    vendor_address: VendorAddress

    customer_name: str

    total_amount: float

    tax_amount: float

    status: InvoiceStatus

    notes: Optional[str] = None

    line_items: List[LineItem]