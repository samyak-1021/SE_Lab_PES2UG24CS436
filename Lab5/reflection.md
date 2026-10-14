# Lab 5 - Reflection

**Name:** Samyak Sanklecha
**SRN:** PES2UG24CS436

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

Easiest were the Flake8 ones and the Pylint style stuff: blank lines, the long line, unused imports, renaming `printSales` to `print_sales`, adding docstrings. They're mechanical and the tool tells you the exact line.

Hardest was the `eval` in `apply_promo_code`. Just deleting it would break the promo feature, so I had to figure out what input it was actually meant to take (`total * 0.9`, `total - 50`) and write a small parser that only accepts that. Getting rid of the `global` was also a bit of work since I had to move the state into a class and change how `main()` calls everything. The logic bugs (negative quantity, string quantity, negative tax) were hard in a different way because no tool pointed at them. I only saw them by running the program and noticing a bill of -630.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

Kind of. Bandit B311 says `random` isn't safe for "security/cryptographic purposes", but a receipt number isn't a security thing, so the reason it gives doesn't really apply here. I still changed it because random numbers can repeat and two receipts with the same number is a real bug.

Another one is Flake8 F841 / Pylint W0612 saying `total` in `apply_promo_code` is unused. It was actually used, just inside the string passed to `eval`, which the tools can't see into. So technically a false positive, but it was pointing at the actual problem anyway.

### 3. How would you integrate static analysis tools into your actual software development workflow?

- Run Flake8 and Pylint locally before committing, using a pre-commit hook so I don't forget.
- Add all three tools to CI (GitHub Actions) on every pull request, and fail the build on any Bandit Medium/High or if the Pylint score drops below something like 9.
- Keep a config file (`.pylintrc` / `setup.cfg`) in the repo so everyone on the team gets the same rules.
- Treat Bandit findings as must-fix before merge, while style warnings can be cleaned up as we go.

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- Pylint went from 5.65 to 10.00, Bandit from 3 issues to 0, Flake8 from 12 to 0.
- The promo code can't run arbitrary code anymore. Earlier, typing `__import__('os').getcwd()` printed my folder path. Now it just says "Promo not applied: Invalid promo code".
- Bad bills are rejected with a clear reason instead of silently giving wrong totals (the -630 bill and the 0 bills are gone).
- Totals print as proper money (`113.4`, `126.00`) instead of `301.45500000000004`.
- The code is easier to read: one class holds the till state, every function has a docstring, and the log file is closed properly.

The main thing I learnt is that the tools catch a lot but not everything. A 10/10 Pylint score didn't fix the negative bill. I had to actually run the program to find that.
