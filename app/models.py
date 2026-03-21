from dataclasses import dataclass, field
from typing import List
import numpy as np


@dataclass
class Asset:
    """Represents a single asset in a portfolio."""
    name: str
    mu: float       # Expected annual return (decimal, e.g. 0.10 = 10%)
    sigma: float    # Annual volatility (decimal, e.g. 0.20 = 20%)
    weight: float   # Portfolio weight (0–1)

    def validate(self):
        if not (0 < self.weight <= 1):
            raise ValueError(f"Weight for {self.name} must be between 0 and 1.")
        if self.sigma <= 0:
            raise ValueError(f"Volatility for {self.name} must be positive.")


@dataclass
class Portfolio:
    """Multi-asset portfolio container."""
    assets: List[Asset] = field(default_factory=list)
    initial_value: float = 100_000.0

    def validate_weights(self):
        total = sum(a.weight for a in self.assets)
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Weights must sum to 1.0. Current sum: {total:.4f}")

    @property
    def mu_vector(self) -> np.ndarray:
        return np.array([a.mu for a in self.assets])

    @property
    def sigma_vector(self) -> np.ndarray:
        return np.array([a.sigma for a in self.assets])

    @property
    def weight_vector(self) -> np.ndarray:
        return np.array([a.weight for a in self.assets])

    @property
    def portfolio_mu(self) -> float:
        return float(np.dot(self.weight_vector, self.mu_vector))

    @property
    def portfolio_sigma(self) -> float:
        return float(np.dot(self.weight_vector, self.sigma_vector))


@dataclass
class SimulationResult:
    """Stores the output of a Monte Carlo simulation run."""
    paths: np.ndarray            # shape: (n_simulations, n_steps)
    final_values: np.ndarray     # shape: (n_simulations,)
    mean: float
    std: float
    min_val: float
    max_val: float
    var_95: float                # Value at Risk at 95% confidence
    var_99: float                # Value at Risk at 99% confidence
    initial_value: float

    @property
    def var_95_pct(self) -> float:
        return ((self.var_95 - self.initial_value) / self.initial_value) * 100

    @property
    def var_99_pct(self) -> float:
        return ((self.var_99 - self.initial_value) / self.initial_value) * 100

    @property
    def mean_return_pct(self) -> float:
        return ((self.mean - self.initial_value) / self.initial_value) * 100