from dataclasses import dataclass


@dataclass
class Product:
    name: str = None
    type: str = None
    unit: str = None
    group: str = None
    supplier: str = None
