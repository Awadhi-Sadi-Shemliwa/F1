"""
Download more races with FastF1 and build one lap table for a bigger version of this project.
Run on YOUR laptop (it needs internet and, from FastF1 3.9, your F1 account login):

    python download_more_races.py --years 2023 --out data/laps_multi_race.csv

Every race is cached in ./fastf1_cache, so a second run is fast and can be done offline.
"""
import argparse, os
from getpass import getpass
from pathlib import Path
import pandas as pd
import fastf1

p = argparse.ArgumentParser()
p.add_argument("--years", nargs="+", type=int, default=[2023])
p.add_argument("--out", default="data/laps_multi_race.csv")
args = p.parse_args()

os.environ.setdefault("F1_USERNAME", input("F1 account email: ").strip())
if "F1_PASSWORD" not in os.environ:
    os.environ["F1_PASSWORD"] = getpass("F1 account password: ")

Path("fastf1_cache").mkdir(exist_ok=True)
fastf1.Cache.configure(cache_dir="fastf1_cache")
fastf1.set_log_level("WARNING")

frames = []
for year in args.years:
    schedule = fastf1.get_event_schedule(year, include_testing=False)
    for _, ev in schedule.iterrows():
        try:
            s = fastf1.get_session(year, ev["EventName"], "R")
            s.load(laps=True, telemetry=False, weather=True, messages=False)
        except Exception as e:                      # future races, missing data, etc.
            print(f"skip {year} {ev['EventName']}: {e}")
            continue
        laps = pd.DataFrame(s.laps).copy()
        # attach the weather sample closest to the start of each lap (track temperature etc.)
        w = s.weather_data[["Time", "AirTemp", "TrackTemp", "Humidity", "Rainfall"]].sort_values("Time")
        laps = pd.merge_asof(laps.sort_values("LapStartTime"), w, left_on="LapStartTime", right_on="Time",
                             direction="nearest", suffixes=("", "_weather"))
        laps["Year"], laps["Event"] = year, ev["EventName"]
        laps["RaceLaps"] = laps["LapNumber"].max()
        # durations -> seconds so the CSV is easy to use
        for c in laps.columns:
            if pd.api.types.is_timedelta64_dtype(laps[c]):
                laps[c] = laps[c].dt.total_seconds()
        frames.append(laps)
        print(f"ok   {year} {ev['EventName']}: {len(laps)} laps")

out = pd.concat(frames, ignore_index=True)
Path(args.out).parent.mkdir(parents=True, exist_ok=True)
out.to_csv(args.out, index=False)
print(f"\nSaved {len(out)} laps from {out['Event'].nunique()} races to {args.out}")
print("Next: drop wet races (Rainfall == True), apply the same cleaning as the notebook, and test on unseen circuits.")
