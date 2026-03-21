import json
from flask import Blueprint, render_template, request, flash, redirect, url_for

from app.forms import MonteCarloForm, PortfolioForm
from app.models import Asset, Portfolio
from app.services.monte_carlo import simulate_random_walk
from app.services.portfolio import run_portfolio_simulation
from app.services.analytics import compute_risk_metrics

main_bp = Blueprint("main", __name__)


# ── Index ────────────────────────────────────────────────────────────────────

@main_bp.route("/")
def index():
    return render_template("index.html")


# ── Monte Carlo ──────────────────────────────────────────────────────────────

@main_bp.route("/monte-carlo", methods=["GET", "POST"])
def monte_carlo():
    form = MonteCarloForm()
    result = None

    if form.validate_on_submit():
        try:
            result = simulate_random_walk(
                mu            = form.mu.data or 0.0,
                sigma         = form.sigma.data,
                n_steps       = form.n_steps.data,
                n_paths       = form.n_paths.data,
                initial_value = form.initial_value.data,
            )
        except Exception as exc:
            flash(f"Simulation error: {exc}", "danger")

    return render_template("monte_carlo.html", form=form, result=result)


# ── Portfolio ─────────────────────────────────────────────────────────────────

@main_bp.route("/portfolio", methods=["GET", "POST"])
def portfolio():
    form = PortfolioForm()
    result = None
    charts = None
    metrics = None
    assets_data = None

    if request.method == "POST":
        # Parse dynamic asset rows submitted as JSON in a hidden field
        assets_json = request.form.get("assets_json", "[]")
        try:
            raw_assets = json.loads(assets_json)
        except json.JSONDecodeError:
            flash("Could not parse asset data. Please try again.", "danger")
            raw_assets = []

        if form.validate_on_submit() and raw_assets:
            try:
                assets = [
                    Asset(
                        name   = a["name"],
                        mu     = float(a["mu"]),
                        sigma  = float(a["sigma"]),
                        weight = float(a["weight"]),
                    )
                    for a in raw_assets
                ]

                port = Portfolio(
                    assets        = assets,
                    initial_value = form.initial_value.data,
                )
                port.validate_weights()

                sim_result, charts = run_portfolio_simulation(
                    portfolio     = port,
                    n_simulations = form.n_simulations.data,
                    n_days        = form.n_days.data,
                )
                result  = sim_result
                metrics = compute_risk_metrics(
                    sim_result.final_values,
                    form.initial_value.data,
                )
                assets_data = assets

            except ValueError as ve:
                flash(str(ve), "warning")
            except Exception as exc:
                flash(f"Simulation error: {exc}", "danger")
        elif not raw_assets:
            flash("Please add at least one asset.", "warning")

    return render_template(
        "portfolio.html",
        form        = form,
        result      = result,
        charts      = charts,
        metrics     = metrics,
        assets_data = assets_data,
    )