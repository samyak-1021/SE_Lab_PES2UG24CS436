"""Retail point-of-sale script.

Totals a cart with tax, applies promo codes, keeps a running sales total
and appends receipts to pos_log.txt.
"""

import itertools
import operator
import re

PRICE_LIST = {"pen": 10, "notebook": 45, "bag": 799, "bottle": 150}
PROMO_PATTERN = re.compile(r"^\s*total\s*([*-])\s*(\d+(?:\.\d+)?)\s*$")
PROMO_OPS = {"*": operator.mul, "-": operator.sub}


class PosTerminal:
    """Holds the running sales state of one till."""

    def __init__(self):
        self.sales_total = 0
        self.receipt_lines = []
        self.stock = dict.fromkeys(PRICE_LIST, 0)
        self._receipt_ids = itertools.count(1001)

    def process_checkout(self, cart_items, tax_rate=0.05, receipts=None):
        """Total a cart of (item, qty) pairs with tax and record a receipt.

        Raises ValueError for an unknown item, a non-positive or
        non-integer quantity, or a tax rate outside 0..1.
        """
        if not 0 <= tax_rate <= 1:
            raise ValueError(f"Invalid tax rate: {tax_rate}")
        subtotal = 0
        for item, qty in cart_items:
            if item not in PRICE_LIST:
                raise ValueError(f"Unknown item: {item}")
            if not isinstance(qty, int) or qty <= 0:
                raise ValueError(f"Invalid quantity for {item}: {qty!r}")
            subtotal += PRICE_LIST[item] * qty
        total = round(subtotal * (1 + tax_rate), 2)
        if receipts is not None:
            receipts.append(total)
        self.sales_total = round(self.sales_total + total, 2)
        self.receipt_lines.append(
            f"Receipt #{next(self._receipt_ids)} total={total:.2f}"
        )
        return total

    def apply_promo_code(self, code_str):
        """Apply a promo like 'total * 0.9' or 'total - 50' to sales."""
        match = PROMO_PATTERN.match(code_str)
        if not match:
            raise ValueError(f"Invalid promo code: {code_str}")
        op, amount = match.groups()
        if op == "*" and float(amount) > 1:
            raise ValueError(f"Discount factor must be at most 1: {amount}")
        discounted = PROMO_OPS[op](self.sales_total, float(amount))
        return round(max(discounted, 0.0), 2)

    def save_receipt_log(self, file="pos_log.txt"):
        """Append pending receipt lines to the log file, then clear them."""
        with open(file, "a", encoding="utf-8") as log:
            for line in self.receipt_lines:
                log.write(line + "\n")
        self.receipt_lines.clear()

    def print_sales(self):
        """Print the running sales total."""
        print(f"Sales so far: {self.sales_total:.2f}")

    def update_stock(self, item, qty):
        """Add qty units of a known item to stock."""
        if item not in PRICE_LIST:
            raise ValueError(f"Unknown item: {item}")
        self.stock[item] += qty
        print("Stock updated for", item, "by", qty)


def main():
    """Run a few sample bills and an interactive promo code."""
    pos = PosTerminal()
    bills = [
        ([("pen", 3), ("notebook", 2)], 0.05),
        ([("bag", 1), ("laptop", 1)], 0.05),
        ([("bottle", -4)], 0.05),
        ([("pen", "2")], -1),
    ]
    for number, (cart, tax_rate) in enumerate(bills, start=1):
        try:
            print(f"Bill {number}:", pos.process_checkout(cart, tax_rate))
        except ValueError as err:
            print(f"Bill {number} rejected: {err}")
    try:
        pos.update_stock("laptop", 5)
    except ValueError as err:
        print("Stock not updated:", err)
    print("After promo:", pos.apply_promo_code("total * 0.9"))
    code = input("Enter promo code (e.g. total - 50): ") or "total - 50"
    try:
        print("After your promo:", pos.apply_promo_code(code))
    except ValueError as err:
        print("Promo not applied:", err)
    pos.save_receipt_log()
    pos.print_sales()


if __name__ == "__main__":
    main()
