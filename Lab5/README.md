# Lab 5 - Static Code Analysis

**Name:** Samyak Sanklecha
**SRN:** PES2UG24CS436
**Assigned repo:** [L5_02_retail_pos](https://github.com/SETAPESU26/L5_02_retail_pos) (`pos_system.py`, retail point of sale)

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.65/10 | **10.00/10** |
| Bandit | 3 issues (1 Medium, 2 Low) | **0** |
| Flake8 | 12 issues | **0** |

## Folder

```
Lab5/
├── before/                  original code
│   ├── pos_system.py
│   ├── pylint_report.txt
│   ├── bandit_report.txt
│   ├── flake8_report.txt
│   └── screenshots/
├── after/                   fixed code
│   ├── pos_system.py
│   ├── pylint_report.txt
│   ├── bandit_report.txt
│   ├── flake8_report.txt    (empty = no issues)
│   └── screenshots/
├── issues.md                issue table + how each one was fixed
└── PES2UG24CS436_SE_Lab5.pdf
```

Fixes are in separate commits: one for Bandit, one for Flake8, one for Pylint, and one for logic bugs the tools didn't catch.

## Before vs After

### Running the program

Before: bill 3 is -630, bill 4 is 0, and laptop (not in the price list) gets billed at 0.

![before run](before/screenshots/01_run.png)

After: bad bills get rejected with a reason.

![after run](after/screenshots/01_run.png)

### Pylint

Before: 5.65/10

![before pylint](before/screenshots/02_pylint.png)

After: 10.00/10

![after pylint](after/screenshots/02_pylint.png)

### Bandit

Before: 3 issues. B307 `eval` (Medium), B311 `random` (Low), B110 try/except/pass (Low)

![before bandit](before/screenshots/03_bandit.png)

After: no issues

![after bandit](after/screenshots/03_bandit.png)

### Flake8

Before: 12 issues (blank lines, unused imports, bare except, long line)

![before flake8](before/screenshots/04_flake8.png)

After: clean

![after flake8](after/screenshots/04_flake8.png)

### Commits

![git log](after/screenshots/05_git_log.png)

## Run it

```bash
pip install pylint bandit flake8
cd after
python pos_system.py
pylint pos_system.py > pylint_report.txt
bandit -r pos_system.py > bandit_report.txt
flake8 pos_system.py > flake8_report.txt
```
