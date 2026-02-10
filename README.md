# Market Risk Analysis Engine (VaR)

## Project Overview
This project was developed to simulate and automate the risk measurement techniques I analyzed during my internship at **Indian Bank (Risk Management Department)**. 

The tool performs a comparative analysis of two primary Value at Risk (VaR) methodologies:
1. **Historical Simulation:** Uses actual past return distributions.
2. **Variance-Covariance (Parametric):** Assumes a normal distribution of returns.

## Features
- **Data Processing:** Automates the calculation of logarithmic daily returns from raw closing prices.
- **Statistical Analysis:** Computes Volatility, Z-scores, and Confidence Intervals (95%/99%).
- **Visualization:** Plots the return distribution with dynamic VaR thresholds to visually identify tail risk.

## Technologies Used
- Python (Pandas, NumPy, SciPy)
- Matplotlib (for financial visualization)

## How to Run
1. Upload your time-series data as `market_data.xlsx`.
2. Run `risk_analysis.py`.
