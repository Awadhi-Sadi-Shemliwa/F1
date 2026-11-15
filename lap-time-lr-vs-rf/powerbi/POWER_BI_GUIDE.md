# Power BI guide: F1 Lap-Time Lab (Linear Regression vs Random Forest)

**Report:** *F1 Lap Time - LR vs Random Forest* in **My workspace** (Power BI service, app.powerbi.com).
**Semantic model:** *F1 LapTime LR vs RF*, built from `powerbi/F1_PowerBI_data.xlsx`.

Everything below was done in the Power BI **web service** with the **new ribbon** switched on (top right of the editor). No Power BI Desktop is needed.

---

## Part A: Get the project results into Power BI

### Step 1: Export the model results from Python to Excel
Power BI cannot run scikit-learn, so the machine learning stays in Python and Power BI shows the results. `make_pbi.py` writes five sheets to `F1_PowerBI_data.xlsx` and formats each one as an **Excel Table**. Power BI reads tables cleanly: correct headers and types.

| Table | Rows | What it holds | Why |
|---|---|---|---|
| **Laps** | 862 | One row per clean lap: driver, team, lap, compound, tyre life, gap, actual lap time and both models' predictions | Master lap list |
| **Predictions** | 1,724 | The same laps in **long format**: one row per lap *per model*, with `Model`, `Predicted_CV`, `Predicted_Forecast`, `Error_CV`, `AbsError_CV`, `RacePhase` | Long format lets one `Model` field drive slicers, legends and small multiples |
| **Metrics** | 4 | RMSE / MAE / R² for each model on each test (random hold-out, forecast laps 39-51) | Headline results table |
| **FeatureImportance** | 14 | Permutation importance per feature per model | Explains *how* each model predicts |
| **Scenario** | 120 | Predicted Ferrari lap-30 lap time for tyre ages 1-30, Medium vs Hard, per model | The "prediction" story |

> `Predicted_CV` is an **out-of-fold** prediction (5-fold cross-validation). Every lap is predicted by a model that never saw it, so the errors in the dashboard are honest test errors, not training errors.

### Step 2: Upload the workbook
1. app.powerbi.com → **Create** (left bar) → **Excel**.
2. In **Connect to data source**, choose **Upload file** → **Browse…** → pick `F1_PowerBI_data.xlsx`. It goes to your OneDrive and the connection is created automatically (Organizational account).
3. **Next**. You'll see every sheet twice. Tick the five items with the **table icon** (`FeatureImportance`, `Laps`, `Metrics`, `Predictions`, `Scenario`), not the sheet versions ending in a number.
4. **Transform data** opens Power Query. The types are already detected (see *Changed column type* under Applied steps). No cleaning is needed, because it was done in Python.
5. **Create a report** → name the semantic model `F1 LapTime LR vs RF` → **Create**.

---

## Part B: Build the visuals

### Four tricks that make building in the browser fast
1. **Tick, don't drag.** Pick a visual type, then tick fields in the Data pane. Power BI places them in the right well (categories go to the axis, numbers to values, a second category to Legend or Small multiples).
2. **"Move to".** If a field lands in the wrong well (e.g. `LapNumber` lands in Y-axis as *Sum of LapNumber*), click the **⌄** on that field → **Move to** → **X-axis**.
3. **Sum → Average.** Same **⌄** menu → **Average**. Use this whenever a number should be averaged across laps (errors, lap times). Then **Rename for this visual** to give it a readable label.
4. **Exact layout.** Format pane (paintbrush) → **General** → **Properties** → type **Height, Width, Horizontal, Vertical**. This is more precise than dragging. Hidden visuals are reachable through **View → Selection pane**.

### Page 1: "Model comparison" (canvas 1920 × 1200)
| # | Visual | Fields | Settings | What it shows |
|---|---|---|---|---|
| 1 | Slicer | `Predictions[Model]` | List | Pick one or both models |
| 2 | Slicer | `Predictions[Driver]` | Style **Dropdown** (20 drivers) | Drill into one driver |
| 3 | Slicer | `Predictions[Compound]` | Style **Tile** | Hard vs Medium laps |
| 4 | Slicer | `Predictions[RacePhase]` | Style **Tile** | Training laps (2-38) vs forecast laps (39-51) |
| 5 | Clustered column | X: `Model`, Y: **Average** `AbsError_CV` renamed *Mean absolute error (s)* | Data labels on; RF column orange | RF 0.22 s vs LR 0.29 s |
| 6 | Line chart | X: `LapNumber`, Y: Avg `AbsError_CV`, Legend: `Model` | RF line orange | Where in the race each model struggles |
| 7 | Table | `Metrics`: Model, Test, RMSE, MAE, R² | Totals **off** (a summed RMSE is meaningless); font 11 | Headline numbers |
| 8 | Line chart | X: `LapNumber`, Y: Avg `LapTime_s` (*Actual*) and Avg `Predicted_CV` (*Predicted*), **Small multiples:** `Model` | Small multiples 2 rows × 1 column; Actual line white | RF follows the actual laps more closely |
| 9 | Scatter | Values: `LapID`, X: `LapTime_s`, Y: `Predicted_CV`, Legend: `Model` | RF markers orange | Tighter diagonal = better model |

### Page 2: "Forecast & prediction"
| # | Visual | Fields | What it shows |
|---|---|---|---|
| 1 | Line chart (small multiples by `Model`) | X: `LapNumber`; Y: Avg `LapTime_s` (*Actual*) and Avg `Predicted_Forecast` (*Forecast*) | Models trained on laps 2-38 only. From lap 39 the forest stops tracking while linear regression keeps the trend |
| 2 | Clustered bar | `FeatureImportance`: Y `Feature`, X `Importance_s`, Legend `Model` | LR relies on fuel (LapNumber) and TyreLife; RF also uses position, team and compound |
| 3 | Line chart (small multiples by `Model`) | `Scenario`: X `TyreLife`, Y `PredictedLapTime_s`, Legend `Compound` | LR draws straight degradation lines; RF a stepped curve. Hard (white) beats Medium (yellow) |

Rename pages by double-clicking the page tab, or through Format page → **Page information → Name**.

---

## Part C: Interactive features

* **Slicers** filter every visual built on `Predictions` (try Driver = SAI and RacePhase = *Forecast laps*).
* **Cross-filtering:** click a column, line point or legend entry and the other visuals on the page highlight that selection.
* **Tooltips:** hover any point, e.g. a scatter dot shows the lap (`LapID`), actual and predicted time.
* **Page navigator** (Insert → Buttons → Navigator → **Page navigator**): buttons in the header switch pages. In editing mode, Ctrl+click a button to follow it.
* **Focus mode / See data:** the ⤢ and ⋯ icons above each visual.

---

## Part D: The F1 night-race look

### Step 1: Import the theme (one file restyles everything)
**Design → Import theme →** `powerbi/assets/F1_Night_Race_theme.json`.
The theme sets:
* Dark background `#0A0D13`.
* Semi-transparent card panels (`#121824`, 12 % transparency) with rounded borders (radius 12) and drop shadows.
* Light text and grid colours.
* Slicer and table styling.
* Data colours **#38A3FF (blue = Linear Regression)**, **#FF7A2F (orange = Random Forest)** and **#E10600 (F1 red)**.

Colours you chose from the *theme* palette follow the theme automatically. Black lines become invisible on dark, so change them to white (Format visual → Lines → Series → Color).

### Step 2: Make room for a header
1. Format page → **Canvas settings → Type: Custom**.
2. Set Width **1920**, Height **1200**.
3. Click an empty part of the canvas → **Ctrl+A** (selects every visual) → drag one visual down by about 120 units. All the selected visuals move together.

### Step 3: Page background (header band, chequered flag, kerb, colour glows)
1. **Design → Page background** → Canvas background → **Image → Browse…**.
2. Pick `powerbi/assets/bg_page1_model_comparison.png` (page 1) or `bg_page2_forecast.png` (page 2).
3. Set **Image fit: Fit**, **Transparency: 0 %**.

The images are made by `powerbi/make_assets.py`. Edit the titles there and re-run to change them.

### Step 4: The animated race strip
* **Insert → Image** → Format image → **Style → Image → Browse…** → `powerbi/assets/race_strip.svg`.
* General → Title **off**; size **760 × 96** at **(780, 6)**.
* It is an **animated SVG**: a blue *LR* car and an orange *RF* car swapping the lead, scrolling track markings and kerbs, spinning wheels, and five "lights out" start lights. Browsers play SVG animations inside images, so it moves in the Power BI service.
* `race_strip.gif` is a GIF version of the same idea, in case you ever need a raster file.
* To change it, edit `powerbi/make_race_svg.py` (colours, speed in `dur=`, car labels) and re-upload.

### Step 5: Page navigator in the header
Insert → Buttons → Navigator → Page navigator → General: Title **off**, size **350 × 64** at **(1556, 22)**. Repeat on page 2 (or copy and paste it).

### Step 6: Save, then view
**Home → Save**, then **Editing ▾ → Viewing** to see what your audience sees.

---

## Files in this folder
| File | Purpose |
|---|---|
| `powerbi/F1_PowerBI_data.xlsx` | Data loaded into Power BI |
| `powerbi/assets/F1_Night_Race_theme.json` | Report theme |
| `powerbi/assets/bg_page1_model_comparison.png`, `bg_page2_forecast.png`, `bg_generic.png` | Page backgrounds |
| `powerbi/assets/race_strip.svg` (+ `.gif`) | Animated header strip |
| `powerbi/make_assets.py`, `powerbi/make_race_svg.py` | Regenerate the styling assets |

## Troubleshooting
* **Field in the wrong well** → ⌄ → Move to.
* **Axis starts at 0 and flattens the lines** → Format → Y-axis → Range (or leave on Auto with small multiples).
* **Can't click a visual hidden behind another** → View → Selection pane.
* **Theme didn't recolour a series** → that colour was set manually. Re-pick it from the theme palette (top row), or Reset to default.
* **Animation not moving** → check you uploaded the `.svg`, not a PNG preview, and that you're in the browser (static exports such as PDF can't animate).
