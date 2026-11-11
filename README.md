# F1 — Grid Position and Points Analysis

A portfolio project investigating how Formula 1 starting-grid position relates to points finishes, and whether the cost of a grid penalty differs by car strength.

The analysis covers 2014–2025 race starts and uses earlier team and driver performance as form features.

## Project files

- [Analysis notebook](f1_grid_to_points_analysis.ipynb)
- [Interactive walkthrough](https://awadhi-sadi-shemliwa.github.io/F1/f1_grid_to_points_animation.html)
- [Original project notes](f1_grid_to_points_README.md)

## Headline result

The project reports a ROC AUC of about 0.85 using grid position alone and about 0.87 with additional features. Its analysis finds that front-runners starting 11th–15th scored points more often than other cars in that grid band.

## Data and scope

The analysis uses F1DB race data, licensed CC BY 4.0. Its conclusions describe the selected seasons and should not be read as causal estimates of the effect of a grid penalty.

## Reproduction note

This starter repository contains the supplied notebook, HTML walkthrough, and project notes. Reproducing the analysis may also require the data-download script, dataset files, dependencies, and generated results and figures.
