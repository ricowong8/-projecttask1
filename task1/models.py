from abc import ABC, abstractmethod
from typing import Optional


# ──────────────────────────────────────────────
# Abstract Base
# ──────────────────────────────────────────────
class Item(ABC):
    def __init__(self, item_id: str, name: str, price: float):
        self.item_id = item_id
        self.name = name
        self.price = price

    @abstractmethod
    def get_info(self) -> str: ...

    def __repr__(self) -> str:
        return self.get_info()


# ──────────────────────────────────────────────
# Product
# ──────────────────────────────────────────────
class Product(Item):
    def __init__(
        self, item_id: str, name: str, price: float, quantity: int, category: str
    ):
        super().__init__(item_id, name, price)
        self._quantity = quantity
        self.category = category

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if value < 0:
            raise ValueError(f"Quantity cannot be negative (got {value}).")
        self._quantity = value

    def update_quantity(self, delta: int):
        """增減數量；delta 可為負數"""
        self.quantity = self._quantity + delta

    # 保留舊方法名，確保 gui.py 相容
    def get_quantity(self) -> int:
        return self._quantity

    def set_quantity(self, value: int):
        self.quantity = value

    def get_info(self) -> str:
        return (
            f"[{self.item_id}] {self.name} | "
            f"${self.price:.2f} | Qty: {self._quantity} | "
            f"Category: {self.category}"
        )


# ──────────────────────────────────────────────
# Inventory
# ──────────────────────────────────────────────
class Inventory:
    def __init__(self):
        self._products: dict[str, Product] = {}

    # ── CRUD ──────────────────────────────────
    def add_product(self, product: Product) -> bool:
        """新增產品；ID 重複回傳 False"""
        if product.item_id in self._products:
            return False
        self._products[product.item_id] = product
        return True

    def remove_product(self, item_id: str) -> bool:
        return self._products.pop(item_id, None) is not None

    def update_product(
        self,
        item_id: str,
        new_price: Optional[float] = None,
        new_quantity: Optional[int] = None,
    ) -> bool:
        p = self._products.get(item_id)
        if not p:
            return False
        if new_price is not None:
            p.price = new_price
        if new_quantity is not None:
            p.quantity = new_quantity
        return True

    def search_product(self, item_id: str) -> Optional[Product]:
        return self._products.get(item_id)

    # ── 查詢 / 統計 ───────────────────────────
    def list_all_products(self) -> list[str]:
        return [p.get_info() for p in self._products.values()]

    def category_summary(self) -> dict[str, int]:
        summary: dict[str, int] = {}
        for p in self._products.values():
            summary[p.category] = summary.get(p.category, 0) + p.quantity
        return summary

    def total_quantity(self) -> int:
        return sum(p.quantity for p in self._products.values())

    def avg_price(self) -> float:
        if not self._products:
            return 0.0
        return sum(p.price for p in self._products.values()) / len(self._products)

    def category_count(self) -> int:
        return len({p.category for p in self._products.values()})

    def low_stock_count(self, threshold: int = 10) -> int:
        return sum(1 for p in self._products.values() if p.quantity < threshold)

    @property
    def products(self) -> dict[str, Product]:
        """唯讀字典視圖，供 GUI 層讀取"""
        return self._products
