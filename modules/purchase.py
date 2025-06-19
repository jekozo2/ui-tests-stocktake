from dataclasses import dataclass
from datetime import datetime

from modules.product import Product


@dataclass
class Purchase:
    supplier: str = None
    purchase_date: datetime = None
    purchase_type: str = None
    reference: str = None
    products: list[Product] = None
    unify_same_items: bool = None
