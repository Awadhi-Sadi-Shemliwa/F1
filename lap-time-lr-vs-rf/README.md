# F1 lap-time prediction: Linear Regression vs Random Forest

![Animated race strip: LR car vs RF car](powerbi/assets/race_strip.gif)

Can a computer predict how fast an F1 car will lap? Two models, 862 laps from the 2023 Italian Grand Prix (Monza), and an interactive Power BI dashboard. Watch `video/F1_PowerBI_walkthrough.mp4` for the 2-minute tour.


| File | What it is |
|---|---|
| `F1_LapTime_LR_vs_RF.ipynb` | The full worked project, already run: data loading, variable choice and leakage check, cleaning, feature engineering, 15 figures each with *why it was made* and *what it shows*, tuning, test results, significance tests, forecasting test, prediction, benchmark against the reference paper, extension, conclusions and references. |
| `poster/F1_LapTime_LR_vs_RF_Poster.pdf` | A0 landscape poster (1189 × 841 mm). `poster.html` is its editable source: change text there and re-export. |
| `figures/` | All figures at 200 dpi (fig01–fig15). |
| `data/monza2023_laps_clean.csv` | The 862 cleaned laps used for modelling. |
| `download_more_races.py` | Downloads every race of a season (plus weather) into one CSV, so you can scale the project up. Run it on your laptop; it asks for your F1 account login. |
| `powerbi/` | Power BI data workbook, step-by-step guide (`POWER_BI_GUIDE.md`), theme, backgrounds and the animated race strip. |
| `video/F1_PowerBI_walkthrough.mp4` | 2-minute captioned walkthrough (compressed copy) of the interactive dashboard (both pages, slicers, drivers, tooltips). `make_video.py` rebuilds it from screenshots. |
| `LinkedIn_post.md` | Plain-English summary of the project, written as a LinkedIn post. |

## Re-running
```
pip install fastf1 scikit-learn seaborn statsmodels scipy
jupyter notebook F1_LapTime_LR_vs_RF.ipynb      # Kernel > Restart & Run All
```
The notebook loads the 2023 Italian GP through FastF1. The FastF1 cache is not in this repository, so the first run needs internet to download the session (the cleaned laps are also in `data/monza2023_laps_clean.csv`). Results are seeded (`SEED = 42`) and should reproduce exactly. Only the timing numbers will change slightly from run to run.

## Headline results
| | Linear Regression (M2) | Random Forest |
|---|---|---|
| Test RMSE, random hold-out | 0.378 s | **0.301 s** |
| Test R² | 0.715 | **0.819** |
| Forecast RMSE, laps 39–51 | **0.449 s** | 0.528 s |

RF is better at interpolation (−20 % RMSE, p < 10⁻⁶). LR is better at forecasting unseen tyre ages (−15 %) and is interpretable. The LR + RF-on-residuals hybrid is best on both tests.
