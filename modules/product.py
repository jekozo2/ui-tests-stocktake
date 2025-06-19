from dataclasses import dataclass

from requests import Response


@dataclass
class Product:
    id: int = None
    name: str = None
    type_id: str = None
    type: str = None
    unit_id: str = None
    unit: str = None
    group_id: str = None
    group: str = None
    supplier_id: str = None
    supplier: str = None
    quantity: int = None
    cost: float = None

    @staticmethod
    def parse_response_to_product(response: Response):
        data = response.json()
        return Product(
            id=data['id'],
            name=data['name'],
            type_id=data['type_id'],
            type=data['type'],
            unit_id=data['unit_id'],
            unit=data['unit'],
            group_id=data['group_id'],
            group=data['group'],
            supplier_id=data['supplier_id'],
            supplier=data['supplier'],
        )
