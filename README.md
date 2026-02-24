# statssheets

M&V statistics scripts, Jupyter notebooks, and reference spreadsheets for the CMVP Capstone.

## Notebooks (open in Colab)

| # | Topic | Open |
|---|-------|------|
| 01 | Descriptive Statistics — fixture wattage sampling | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jskromer/statssheets/blob/main/notebooks/01_descriptive_stats.ipynb) |
| 02 | OLS Regression via Matrix Algebra | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jskromer/statssheets/blob/main/notebooks/02_least_squares.ipynb) |
| 03 | Sampling Methodology & Sample Size Calculator | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jskromer/statssheets/blob/main/notebooks/03_sampling_exercise.ipynb) |
| 04 | M&V Plan Builder (Greenfield Municipal Center) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jskromer/statssheets/blob/main/notebooks/04_mv_plan_builder.ipynb) |

## Scripts (CLI)

Run standalone from the command line — no Jupyter required.

```bash
python scripts/descriptive_stats.py
python scripts/least_squares_matrix.py
python scripts/sampling_exercise.py
python scripts/mv_plan_builder.py --greenfield
```

## Spreadsheets

Original Excel reference files in `spreadsheets/`. The Python scripts and notebooks replicate these step by step.

| File | Purpose |
|------|---------|
| Descriptive Stats Step 1.xlsx | Mean, variance, std dev, CV from fixture sample |
| Least_Squares_Matrix_Formula.xlsx | OLS via X′X, X′Y matrix construction |
| Statistics_Exercise.xlsm | Population generation, sampling, sample size calc |
| OEH_M&V_planning tool.xlsx | M&V plan template (team, design, budget, tasks) |

## Related

- [CMVP Capstone](https://cmvp-capstone.vercel.app) — interactive M&V workbench
- [Counterfactual Designs](https://cfdesigns.vercel.app) — course modules
- [Learning Path](https://mv-classmap.vercel.app) — progress tracker
- [IPMVP Reference](https://mv-course.vercel.app) — protocol translation guide
