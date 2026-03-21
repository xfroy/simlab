"""
analytics.py
------------
Risk and statistical analytics utilities.
"""

import numpy as np
from scipy import stats as scipy_stats
from app.models import SimulationResult


def compute_risk_metrics(final_values: np.ndarray,
                         initial_value: float) -> dict:
    """
    Compute comprehensive risk metrics from an array of final simulation values.

    Returns a flat dict suitable for template rendering.
    """
    returns = (final_values - initial_value) / initial_value

    mean_val  = float(np.mean(final_values))
    std_val   = float(np.std(final_values))
    var_95    = float(np.percentile(final_values, 5))
    var_99    = float(np.percentile(final_values, 1))
    cvar_95   = float(np.mean(final_values[final_values <= var_95]))
    cvar_99   = float(np.mean(final_values[final_values <= var_99]))

    skewness  = float(scipy_stats.skew(final_values))
    kurtosis  = float(scipy_stats.kurtosis(final_values))   # Excess kurtosis

    prob_profit = float(np.mean(final_values > initial_value) * 100)
    prob_loss   = float(np.mean(final_values < initial_value) * 100)

    best_case   = float(np.percentile(final_values, 95))
    worst_case  = float(np.percentile(final_values, 5))
    median_val  = float(np.median(final_values))

    return {
        # Absolute values
        "mean":       mean_val,
        "std":        std_val,
        "min":        float(np.min(final_values)),
        "max":        float(np.max(final_values)),
        "median":     median_val,
        "var_95":     var_95,
        "var_99":     var_99,
        "cvar_95":    cvar_95,
        "cvar_99":    cvar_99,
        "best_case":  best_case,
        "worst_case": worst_case,

        # Return percentages
        "mean_return_pct":  ((mean_val - initial_value) / initial_value) * 100,
        "var_95_pct":       ((var_95 - initial_value) / initial_value) * 100,
        "var_99_pct":       ((var_99 - initial_value) / initial_value) * 100,
        "cvar_95_pct":      ((cvar_95 - initial_value) / initial_value) * 100,
        "cvar_99_pct":      ((cvar_99 - initial_value) / initial_value) * 100,

        # Distribution shape
        "skewness":         skewness,
        "kurtosis":         kurtosis,
        "prob_profit_pct":  prob_profit,
        "prob_loss_pct":    prob_loss,

        "n_simulations":    len(final_values),
        "initial_value":    initial_value,
    }


def sharpe_ratio(mu: float, sigma: float,
                 risk_free_rate: float = 0.05) -> float:
    """Annualised Sharpe ratio."""
    if sigma == 0:
        return float("inf")
    return (mu - risk_free_rate) / sigma


def sortino_ratio(returns: np.ndarray,
                  risk_free_rate: float = 0.05) -> float:
    """Sortino ratio using downside deviation."""
    excess = returns - risk_free_rate / 252
    downside = excess[excess < 0]
    if len(downside) == 0:
        return float("inf")
    downside_std = np.std(downside) * np.sqrt(252)
    mean_excess  = np.mean(excess) * 252
    return float(mean_excess / downside_std) if downside_std != 0 else float("inf")


def max_drawdown(path: np.ndarray) -> float:
    """
    Maximum drawdown of a single price path.
    Returns a negative number (e.g. -0.25 = 25% drawdown).
    """
    roll_max = np.maximum.accumulate(path)
    drawdown = (path - roll_max) / roll_max
    return float(np.min(drawdown))