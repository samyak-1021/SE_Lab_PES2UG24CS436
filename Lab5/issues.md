# Lab 5 - Issues Found and Fixed

**Name:** Samyak Sanklecha
**SRN:** PES2UG24CS436
**Assigned repo:** [L5_02_retail_pos](https://github.com/SETAPESU26/L5_02_retail_pos) (`pos_system.py`)

Line numbers are from the original file (`reports/before/` has the raw tool output).

## Score summary

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.65/10 (20 messages) | 10.00/10 |
| Bandit | 3 issues (1 Medium, 2 Low) | 0 issues |
| Flake8 | 12 issues | 0 issues |

## Issue table

High and medium first.

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | `eval()` on user input | Bandit B307, Pylint W0123 | Security | High (Bandit: Medium) | 24-27 | The promo code typed by the user goes straight into `eval()`. I typed `__import__('os').getcwd()` and it printed my folder path, so any Python code could run. | Removed `eval`. A regex only accepts `total * <number>` or `total - <number>`, and an `operator` lookup does the maths. Anything else raises `ValueError`. |
| 2 | Bare `except` hiding wrong bills | Pylint W0702, Flake8 E722 | Bug | High | 14-17 | Any error while adding an item was swallowed and added 0. So `laptop` (not in price list) was billed at 0, and qty `"2"` (a string) made bill 4 come out as 0. | Validate each line before adding: unknown item or bad quantity raises `ValueError` and the bill gets rejected instead of silently going wrong. |
| 3 | Negative quantity and negative tax accepted | None (found by running it) | Bug | High | 47-48 | Bill 3 (`bottle, -4`) came out as **-630**, and `tax_rate=-1` wipes the bill to 0. Tools don't catch this since it's valid Python. | Quantity must be a positive int and `tax_rate` must be between 0 and 1, otherwise `ValueError`. |
| 4 | Mutable default argument | Pylint W0102 | Bug | Medium | 10 | `receipts=[]` is created once and shared by every call, so receipts from old calls leak into new ones. | Default changed to `None` and only appended to if the caller passes a list. |
| 5 | Global mutable state | Pylint W0603, C0103 | Design | Medium | 6-8, 11 | `sales_total` was changed through `global`, so any function could change the running total. | Moved the state (`sales_total`, `receipt_lines`, `stock`) into a `PosTerminal` class. |
| 6 | File opened without `with` / no encoding | Pylint R1732, W1514 | Bug | Medium | 37 | `open()` is never closed, so the handle leaks and writes might not flush. Encoding depends on the OS. | `with open(file, "a", encoding="utf-8")`. |
| 7 | `try/except/pass` + `update_stock` that does nothing | Bandit B110, Pylint W0718 | Bug | Medium | 29-34 | It assigned the price to itself (`price_list[item] = price_list[item]`), printed "Stock updated" anyway, and hid errors with `except Exception: pass`. | Added a real `stock` dict. Unknown item raises `ValueError`, which `main()` catches and prints. |
| 8 | `random` used for receipt numbers | Bandit B311 | Security / Bug | Low | 21 | `random.randint(1000, 9999)` can give two receipts the same number. | Sequential numbers using `itertools.count(1001)`, so they're unique in a run. |
| 9 | Float noise in money | None (found by running it) | Bug | Low | 18, 50 | Output like `301.45500000000004`. | Round totals to 2 decimals and print with `:.2f`. |
| 10 | Receipt log duplicates | None (found by reading it) | Bug | Low | 36-39 | `receipt_lines` is never cleared, so calling save twice writes the same receipts twice. | Clear the list after writing. |
| 11 | Unused imports | Flake8 F401, Pylint W0611 | Style | Low | 1, 3 | `json` and `logging` are imported but never used. | Removed. |
| 12 | Unused variable `total` | Flake8 F841, Pylint W0612 | Style | Low | 26 | Only "used" inside the eval string. | Gone with the eval fix. |
| 13 | PEP 8 formatting | Flake8 E302, E305, E501 | Style | Low | 10-56 | Missing 2 blank lines between functions, line 21 was 88 chars. | Added blank lines, wrapped the long line. |
| 14 | Naming, docstrings, old string formatting | Pylint C0103, C0114, C0116, C0209 | Style | Low | 1, 10-44 | `printSales` is camelCase, no docstrings anywhere, `%` formatting. | `print_sales`, added module/class/function docstrings, used f-strings. |
| 15 | `main()` runs on import | None | Design | Low | 56 | Importing the file runs the whole program. | `if __name__ == "__main__":` guard. |

## Commits

1. `Lab5: add original pos_system.py and baseline static analysis reports`
2. `Lab5: fix Bandit issues (B307 eval, B311 random, B110 try-except-pass)`
3. `Lab5: fix Flake8 issues (blank lines, line length, unused imports, bare except)`
4. `Lab5: fix Pylint issues (docstrings, global state, mutable default, with/encoding, naming) - 10.00/10`
5. `Lab5: fix logic bugs not caught by the tools (input validation, money rounding, stock update, duplicate log lines)`

## Output before vs after (default promo)

Before:
```
Bill 1: 126.0
Bill 2: 838.95
Bill 3: -630.0
Bill 4: 0
After promo: 301.45500000000004
After your promo: 284.95000000000005
Sales so far: 334.95000000000005
```

After:
```
Bill 1: 126.0
Bill 2 rejected: Unknown item: laptop
Bill 3 rejected: Invalid quantity for bottle: -4
Bill 4 rejected: Invalid tax rate: -1
Stock not updated: Unknown item: laptop
After promo: 113.4
After your promo: 76.0
Sales so far: 126.00
```
