import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "simlab-dev-secret-2024")
    DEBUG = os.environ.get("DEBUG", "True") == "True"

    # Simulation defaults
    DEFAULT_SIMULATIONS = 1000
    DEFAULT_STEPS = 252          # Trading days in a year
    DEFAULT_INITIAL_PRICE = 100.0

    # Monte Carlo defaults
    MC_DEFAULT_MU = 0.0
    MC_DEFAULT_SIGMA = 1.0
    MC_DEFAULT_STEPS = 200
    MC_DEFAULT_PATHS = 50

    # Portfolio defaults
    PORTFOLIO_DEFAULT_SIMS = 1000
    PORTFOLIO_DEFAULT_DAYS = 252