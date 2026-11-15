# What is a grid place worth in Formula 1?

Every race start from 2014 to 2025 (252 races, 5,069 starts), used to predict a points finish before the lights go out and to price a 10-place grid penalty.

**Business question.** Teams can choose when to take power-unit grid penalties. What does a grid drop cost, and is the price the same for every car?

**Answer in one paragraph.** Grid position alone predicts a points finish with a ROC AUC of 0.85 on 2023 to 2025; adding recent team and driver form gives 0.87. But the price of a bad grid slot depends on the car: front-runners starting 11th to 15th still score points 69% of the time, other cars 29%. A readable logistic model missed that interaction (it predicted 52% for front-runners starting outside the top ten when 66% actually scored); gradient boosting got it right (65%). Front-running teams can afford tactical penalties; midfield teams cannot.

![Penalty cost](figures/fig5_penalty_cost.png)

## What is in this repository

| Path | Contents |
|---|---|
| `src/get_data.py` | Downloads the F1DB CSV release into `data/f1db/` |
| `src/analysis.py` | The whole analysis with `# %%` cells |
| `analysis.ipynb` | The same analysis as an executed notebook |
| `figures/`, `results/metrics.json` | Figures and every number quoted in the paper |
| `paper/paper.md` | Write-up in research-paper format with references |
| `animation.html` | Step-through explanation of the project |

## Run it

```bash
pip install -r requirements.txt
python src/get_data.py
python src/analysis.py
```

The script uses seasons 2014 to 2025. A later F1DB release adds races to later seasons but does not change those.

## Data and credit

[F1DB](https://github.com/f1db/f1db), an open-source Formula 1 database, licensed CC BY 4.0.

## Method in brief

1. **Clean**: finishing position is text (`DNF`, `DNS`, `DSQ`…); 15% of cells become NaN under `to_numeric(errors="coerce")` and each code is handled on purpose. Retirements are results, not gaps. Empty points mean zero. Pit-lane starts are placed behind the field.
2. **Explore**: points probability by grid slot; how tightly grid and finish are linked at each circuit; reliability by season.
3. **Split by season**: train 2014 to 2022, test 2023 to 2025.
4. **Model**: baseline, rule of thumb, logistic regression, gradient boosting. Form features only look backwards.
5. **Evaluate**: ROC AUC, Brier, calibration, permutation importance.
6. **Decide**: observed points by grid band for front-runners and for the rest, then check which model reproduces it.
