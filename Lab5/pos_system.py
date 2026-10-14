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
        self._receipt_ids = itertools.count(1001)

    def process_checkout(self, cart_items, tax_rate=0.05, receipts=None):
        """Total a cart of (item, qty) pairs with tax and record a receipt."""
        subtotal = 0
        for item, qty in cart_items:
            try:
                subtotal = subtotal + PRICE_LIST[item] * qty
            except (KeyError, TypeError):
                subtotal = subtotal + 0
        total = subtotal + subtotal * tax_rate
        if receipts is not None:
            receipts.append(total)
        self.sales_total += total
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
        return PROMO_OPS[op](self.sales_total, float(amount))

    def save_receipt_log(self, file="pos_log.txt"):
        """Append all receipt lines to the log file."""
        with open(file, "a", encoding="utf-8") as log:
            for line in self.receipt_lines:
                log.write(line + "\n")

    def print_sales(self):
        """Print the running sales total."""
        print(f"Sales so far: {self.sales_total}")


def update_stock(item, qty):
    """Update the stock count of an item."""
    if item not in PRICE_LIST:
        print("Cannot update stock, unknown item:", item)
        return
    print("Stock updated for", item, "by", qty)


def main():
    """Run a few sample bills and an interactive promo code."""
    pos = PosTerminal()
    print("Bill 1:", pos.process_checkout([("pen", 3), ("notebook", 2)]))
    print("Bill 2:", pos.process_checkout([("bag", 1), ("laptop", 1)]))
    print("Bill 3:", pos.process_checkout([("bottle", -4)]))
    print("Bill 4:", pos.process_checkout([("pen", "2")], tax_rate=-1))
    update_stock("laptop", 5)
    print("After promo:", pos.apply_promo_code("total * 0.9"))
    code = input("Enter promo code (e.g. total - 50): ") or "total - 50"
    print("After your promo:", pos.apply_promo_code(code))
    pos.save_receipt_log()
    pos.print_sales()


if __name__ == "__main__":
    main()
