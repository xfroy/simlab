"""
monte_carlo.py
--------------
Core Monte Carlo / stochastic-process engine.
Implements Geometric Brownian Motion (GBM) for single-asset random walks.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import io
import base64


def _fig_to_b64(fig: plt.Figure) -> str:
    """Convert a Matplotlib figure to a base64-encoded PNG string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return encoded


def simulate_random_walk(
    mu: float,
    sigma: float,
    n_steps: int,
    n_paths: int,
    initial_value: float,
    dt: float = 1 / 252,
) -> dict:
    """
    Simulate multiple GBM random-walk paths.

    Parameters
    ----------
    mu            : Annualised drift.
    sigma         : Annualised volatility.
    n_steps       : Number of time steps per path.
    n_paths       : Number of independent paths.
    initial_value : Starting price / value.
    dt            : Time increment (default = 1 trading day).

    Returns
    -------
    dict with keys: paths (ndarray), plot_b64 (str), stats (dict)
    """
    np.random.seed(None)  # Fresh randomness each run

    # GBM increments
    Z = np.random.standard_normal((n_paths, n_steps))
    log_returns = (mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z

    # Cumulative product → price paths
    paths = initial_value * np.exp(np.cumsum(log_returns, axis=1))
    # Prepend initial value column
    start_col = np.full((n_paths, 1), initial_value)
    paths = np.hstack([start_col, paths])

    final_values = paths[:, -1]

    stats = {
        "mean":   float(np.mean(final_values)),
        "std":    float(np.std(final_values)),
        "min":    float(np.min(final_values)),
        "max":    float(np.max(final_values)),
        "median": float(np.median(final_values)),
        "var_95": float(np.percentile(final_values, 5)),
    }

    plot_b64 = _plot_paths(paths, stats, n_paths, initial_value)

    return {"paths": paths, "stats": stats, "plot_b64": plot_b64}


def _plot_paths(paths, stats, n_paths, initial_value):
    """Render the random-walk path chart."""
    BG   = "#0d1117"
    GRID = "#21262d"
    ACC  = "#58a6ff"
    MED  = "#f78166"
    TEXT = "#e6edf3"

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
    ax.set_facecolor(BG)

    n_show = min(n_paths, 80)
    alpha  = max(0.08, 0.4 / (n_show ** 0.5))

    for i in range(n_show):
        ax.plot(paths[i], color=ACC, alpha=alpha, linewidth=0.8)

    # Median path
    median_path = np.median(paths, axis=0)
    ax.plot(median_path, color=MED, linewidth=2.0, label="Median path", zorder=5)

    # Initial value reference line
    ax.axhline(initial_value, color=TEXT, linewidth=0.8, linestyle="--",
               alpha=0.5, label=f"Start: {initial_value:,.2f}")

    ax.set_title("Monte Carlo Random Walk", color=TEXT, fontsize=14,
                 fontweight="bold", pad=12)
    ax.set_xlabel("Steps", color=TEXT, fontsize=11)
    ax.set_ylabel("Value", color=TEXT, fontsize=11)
    ax.tick_params(colors=TEXT)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"{x:,.0f}"))
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.grid(True, color=GRID, linewidth=0.5, linestyle="--")
    ax.legend(facecolor=BG, edgecolor=GRID, labelcolor=TEXT, fontsize=9)

    fig.tight_layout()
    return _fig_to_b64(fig)