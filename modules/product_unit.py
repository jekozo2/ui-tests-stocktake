from dataclasses import dataclass


@dataclass
class ProductUnit:
    name: str = None
    unit_yield: float = None
    description: str = None
