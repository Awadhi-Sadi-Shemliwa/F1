# LinkedIn post: F1 Lap-Time Lab

**Attach:** `video/F1_PowerBI_walkthrough.mp4` (2 min 7 s, 1080p).
**Replace** `[GitHub link]` with the URL of your F1 repo before posting.

---

🏎️ Can a computer predict how fast an F1 car will lap?

For my machine learning mini-project, I took 862 real laps from the 2023 Italian Grand Prix at Monza and asked two different models to predict every lap time. Then I turned the results into an interactive Power BI dashboard (video below 👇).

𝗪𝗵𝗮𝘁 𝗱𝗲𝗰𝗶𝗱𝗲𝘀 𝗮 𝗹𝗮𝗽 𝘁𝗶𝗺𝗲?
A few clues: how much fuel is left (a lighter car is faster), how old the tyres are (worn tyres are slower), which tyre type, the car, and the traffic around it.

𝗧𝗵𝗲 𝘁𝘄𝗼 𝗰𝗼𝗻𝘁𝗲𝗻𝗱𝗲𝗿𝘀
🔵 Linear Regression draws one straight-line rule, like "every extra lap on the same tyres costs about 0.07 s". Simple, and easy to explain.
🟠 Random Forest asks hundreds of yes/no questions ("tyres older than 15 laps? Is it a Ferrari?") and averages the answers. Flexible, but it can only repeat patterns it has already seen.

To keep it fair, every lap was predicted by a model that had never seen that lap.

𝗪𝗵𝗮𝘁 𝗜 𝗳𝗼𝘂𝗻𝗱
✅ On normal laps, Random Forest wins. Its typical error is about 0.30 s, roughly 20% better than the straight line (0.38 s).
✅ On "future" laps, Linear Regression wins. Both models learned only from laps 2–38 and then had to predict laps 39–51. The simple rule was about 15% more accurate (0.45 s vs 0.53 s). The forest had never seen tyres that old, so it got stuck.
✅ Combining them gave the best result on both tests: the straight line sets the trend and the forest fixes what it misses.

💡 The lesson: the "smartest" model depends on the question you ask it. Filling in gaps and predicting the future are different jobs.

𝗜𝗻 𝘁𝗵𝗲 𝗱𝗮𝘀𝗵𝗯𝗼𝗮𝗿𝗱 𝘆𝗼𝘂 𝗰𝗮𝗻:
• switch between the two models
• filter by tyre type (e.g. Hard) or by driver (Hamilton, Sainz…)
• compare the race's final 13 laps with the rest
• hover any lap to see the real vs predicted time
• play a what-if: a Ferrari on lap 30, Medium vs Hard tyres

Built with Python (FastF1, scikit-learn) and Power BI. The full notebook, poster, data and dashboard guide are on GitHub: [GitHub link]

#Formula1 #F1 #MachineLearning #DataScience #PowerBI #Python #DataVisualization #RandomForest #LinearRegression #ItalianGP
