"""
portfolio.py
------------
Multi-asset portfolio Monte Carlo simulator using GBM per asset.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import io
import base64

from app.models import Portfolio, SimulationResult


def _fig_to_b64(fig: plt.Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return encoded


# ──────────────────────────────────────────────────────────────────────────────
# Simulation core
# ──────────────────────────────────────────────────────────────────────────────

def run_portfolio_simulation(
    portfolio: Portfolio,
    n_simulations: int = 1000,
    n_days: int = 252,
) -> tuple[SimulationResult, dict]:
    """
    Simulate portfolio value over time using GBM for each asset.

    Returns
    -------
    (SimulationResult, charts_dict)
    charts_dict keys: 'trajectory_b64', 'histogram_b64'
    """
    np.random.seed(None)

    dt = 1 / 252
    n_assets = len(portfolio.assets)
    mu_vec    = portfolio.mu_vector
    sigma_vec = portfolio.sigma_vector
    w_vec     = portfolio.weight_vector

    # Portfolio effective mu & sigma (per day)
    port_mu    = np.dot(w_vec, mu_vec)
    port_sigma = np.dot(w_vec, sigma_vec)

    # GBM simulation: shape (n_simulations, n_days)
    Z = np.random.standard_normal((n_simulations, n_days))
    log_ret = (port_mu - 0.5 * port_sigma ** 2) * dt + port_sigma * np.sqrt(dt) * Z
    cum_ret = np.cumsum(log_ret, axis=1)

    # Price paths
    start_col = np.zeros((n_simulations, 1))
    cum_ret   = np.hstack([start_col, cum_ret])
    paths     = portfolio.initial_value * np.exp(cum_ret)

    final_values = paths[:, -1]

    var_95 = float(np.percentile(final_values, 5))
    var_99 = float(np.percentile(final_values, 1))

    result = SimulationResult(
        paths         = paths,
        final_values  = final_values,
        mean          = float(np.mean(final_values)),
        std           = float(np.std(final_values)),
        min_val       = float(np.min(final_values)),
        max_val       = float(np.max(final_values)),
        var_95        = var_95,
        var_99        = var_99,
        initial_value = portfolio.initial_value,
    )

    charts = {
        "trajectory_b64": _plot_trajectories(paths, result, n_simulations),
        "histogram_b64":  _plot_histogram(final_values, result),
    }

    return result, charts


# ──────────────────────────────────────────────────────────────────────────────
# Charts
# ──────────────────────────────────────────────────────────────────────────────

_BG   = "#0d1117"
_GRID = "#21262d"
_ACC  = "#3fb950"   # Green for portfolio (profit feel)
_WARN = "#f78166"   # Red/orange for VaR
_MED  = "#d2a8ff"   # Purple for median
_TEXT = "#e6edf3"


def _plot_trajectories(paths, result: SimulationResult, n_simulations: int) -> str:
    """Line chart of simulated portfolio paths."""
    fig, ax = plt.subplots(figsize=(11, 5), facecolor=_BG)
    ax.set_facecolor(_BG)

    n_show = min(n_simulations, 150)
    alpha  = max(0.04, 0.3 / (n_show ** 0.5))

    for i in range(n_show):
        ax.plot(paths[i], color=_ACC, alpha=alpha, linewidth=0.7)

    # Median trajectory
    median_path = np.median(paths, axis=0)
    ax.plot(median_path, color=_MED, linewidth=2.0, label="Median", zorder=6)

    # Mean trajectory
    mean_path = np.mean(paths, axis=0)
    ax.plot(mean_path, color="#ffa657", linewidth=1.5,
            linestyle="--", label="Mean", zorder=5)

    ax.axhline(result.initial_value, color=_TEXT, linewidth=0.8,
               linestyle=":", alpha=0.6, label=f"Initial: ${result.initial_value:,.0f}")

    ax.set_title("Portfolio Simulation Paths", color=_TEXT,
                 fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Trading Days", color=_TEXT, fontsize=11)
    ax.set_ylabel("Portfolio Value ($)", color=_TEXT, fontsize=11)
    ax.tick_params(colors=_TEXT)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"${x:,.0f}"))
    for sp in ax.spines.values():
        sp.set_edgecolor(_GRID)
    ax.grid(True, color=_GRID, linewidth=0.5, linestyle="--")
    ax.legend(facecolor=_BG, edgecolor=_GRID, labelcolor=_TEXT, fontsize=9)
    fig.tight_layout()
    return _fig_to_b64(fig)


def _plot_histogram(final_values: np.ndarray, result: SimulationResult) -> str:
    """Histogram of final portfolio values with VaR markers."""
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=_BG)
    ax.set_facecolor(_BG)

    ax.hist(final_values, bins=60, color=_ACC, alpha=0.75, edgecolor=_BG,
            linewidth=0.4)

    ax.axvline(result.var_95, color=_WARN, linewidth=2.0,
               label=f"VaR 95%: ${result.var_95:,.0f}")
    ax.axvline(result.var_99, color="#ff7b72", linewidth=2.0,
               linestyle="--", label=f"VaR 99%: ${result.var_99:,.0f}")
    ax.axvline(result.mean, color=_MED, linewidth=2.0,
               label=f"Mean: ${result.mean:,.0f}")

    ax.set_title("Distribution of Final Portfolio Values", color=_TEXT,
                 fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Final Portfolio Value ($)", color=_TEXT, fontsize=11)
    ax.set_ylabel("Frequency", color=_TEXT, fontsize=11)
    ax.tick_params(colors=_TEXT)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"${x:,.0f}"))
    for sp in ax.spines.values():
        sp.set_edgecolor(_GRID)
    ax.grid(True, color=_GRID, linewidth=0.5, linestyle="--", axis="y")
    ax.legend(facecolor=_BG, edgecolor=_GRID, labelcolor=_TEXT, fontsize=9)
    fig.tight_layout()
    return _fig_to_b64(fig)