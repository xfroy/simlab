# 🚀 SimLab – Monte Carlo & Portfolio Risk Simulator

SimLab is a Python-based quantitative finance simulation platform built with Flask, NumPy, and Matplotlib. It lets you explore uncertainty, model investment risk, and visualize stochastic processes through Monte Carlo methods — the same techniques used by banks and hedge funds.

---

## 🧠 Features

### 🎲 Monte Carlo Simulation (`/monte-carlo`)

* Geometric Brownian Motion (GBM) random walk engine
* Configurable drift (μ), volatility (σ), steps, and paths
* Renders up to 500 simultaneous stochastic paths
* Highlights median path against all simulated trajectories
* Live statistics: Mean, Std, Min, Max, Median, VaR 95%

### 📈 Portfolio Risk Simulator (`/portfolio`)

* Dynamic multi-asset portfolio builder (add/remove assets in the UI)
* Per-asset configuration:
  * Name
  * Expected annual return (μ)
  * Annual volatility (σ)
  * Portfolio weight
* Real-time weight validation (weights must sum to 1.0)
* Runs up to 10,000 simulations over up to 1,260 trading days
* Two output charts: trajectory paths + return distribution histogram

### 📊 Data Visualization

* Dark terminal-style charts (GitHub-dark palette)
* Portfolio trajectory plot — all paths + median + mean overlaid
* Histogram of final portfolio values with VaR zone highlighted
* All charts rendered server-side with Matplotlib and returned as base64 PNG

### ⚠️ Risk Metrics

| Metric | Description |
|---|---|
| Mean | Average final portfolio value across all simulations |
| Std Deviation | Spread / dispersion of outcomes |
| VaR 95% | Value at Risk — only 5% of outcomes are worse than this |
| VaR 99% | Stricter threshold — only 1% of outcomes fall below |
| CVaR 95% / 99% | Conditional VaR — average of the worst outcomes beyond VaR |
| Prob. Profit | % of simulations that ended in profit |
| Skewness | Whether returns skew positive or negative |
| Kurtosis | Fat-tail risk (how extreme the outliers are) |
| Min / Max | Worst and best single simulation outcome |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Web framework | Flask 3.x |
| Forms & validation | Flask-WTF, WTForms |
| Numerical engine | NumPy |
| Statistical analytics | SciPy |
| Data manipulation | Pandas |
| Charting | Matplotlib |
| Language | Python 3.11+ |

---

## 📁 Project Structure

```
simlab/
├── main.py                      # App entry point
├── requirements.txt
└── app/
    ├── __init__.py              # App factory (create_app)
    ├── config.py                # Environment & simulation defaults
    ├── models.py                # Asset, Portfolio, SimulationResult dataclasses
    ├── forms.py                 # WTForms: MonteCarloForm, PortfolioForm
    ├── views.py                 # Routes: /, /monte-carlo, /portfolio
    ├── auth.py                  # Auth blueprint (stubs, ready for Flask-Login)
    ├── services/
    │   ├── __init__.py
    │   ├── monte_carlo.py       # GBM simulation engine + path chart renderer
    │   ├── portfolio.py         # Multi-asset simulator + trajectory & histogram charts
    │   └── analytics.py        # VaR, CVaR, Sharpe, Sortino, max drawdown
    └── templates/
        ├── layout.html          # Base template (dark terminal UI, Space Mono font)
        ├── index.html           # Landing page
        ├── monte_carlo.html     # Monte Carlo simulation page
        └── portfolio.html       # Portfolio simulator with dynamic asset builder
```

---

## ⚙️ Installation

```bash
git clone <your-repo>
cd simlab

pip install -r requirements.txt
python main.py
```

Open `http://localhost:5000`

---

## 🧪 Usage

### Monte Carlo Simulation

1. Navigate to `/monte-carlo`
2. Configure:
   * **μ (drift)** — expected annual return (e.g. `0.05` = 5%)
   * **σ (volatility)** — annual volatility (e.g. `0.20` = 20%)
   * **Steps** — number of time steps per path (e.g. `252` = 1 trading year)
   * **Paths** — number of independent simulations (e.g. `50`)
   * **Initial Value** — starting price
3. Click **Run Simulation**
4. Read the path chart and statistics panel

### Portfolio Risk Simulator

1. Navigate to `/portfolio`
2. Set your **initial capital** (e.g. $100,000)
3. Add assets using the dynamic asset builder:
   * Enter name, μ, σ, and weight for each asset
   * The weight bar turns **green** when weights sum to 1.0
4. Set simulation count and trading days
5. Click **Run Simulation**
6. Analyze:
   * Portfolio trajectory paths (all simulations + median + mean)
   * Return distribution histogram with VaR cutoffs highlighted
   * Full risk metrics table (VaR, CVaR, prob. profit, skewness, kurtosis)

---

## 🧮 The Math (Plain English)

Every price path is generated using **Geometric Brownian Motion (GBM)**:

```
S(t+1) = S(t) × exp((μ - ½σ²)·dt + σ·√dt·Z)
```

Where:
- `μ` = expected annual return (drift)
- `σ` = annual volatility
- `dt` = time increment (1/252 for daily)
- `Z` = random shock drawn from a standard normal distribution

Running this equation 1,000 times in parallel gives you 1,000 different futures — the full distribution of possible outcomes.

---

## 🔥 Future Improvements

* Real stock price data integration (NSE / Yahoo Finance API)
* Correlated asset modeling (Cholesky decomposition on covariance matrix)
* Portfolio optimization — efficient frontier (Markowitz)
* Streamlit version for fully interactive UI without Flask
* REST API endpoints for external access
* User authentication with Flask-Login
* Export simulation results to CSV / PDF report
* Backtesting against historical data

---

## 🧠 Concepts Covered

* Monte Carlo Simulation
* Geometric Brownian Motion (GBM)
* Stochastic Processes
* Value at Risk (VaR) & Conditional VaR (CVaR)
* Quantitative Risk Modeling
* Portfolio Theory
* Probability Distributions
* Financial Statistics (Skewness, Kurtosis, Sharpe Ratio)

---

## 💣 Author

**Maswili** — Building quantitative systems with Python ⚡

> *"Banks pay quants six figures to run this math. We built it in an afternoon."*