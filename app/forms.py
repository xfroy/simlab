from flask_wtf import FlaskForm
from wtforms import (
    FloatField, IntegerField, StringField,
    SubmitField, FieldList, FormField
)
from wtforms.validators import DataRequired, NumberRange, Optional


class AssetForm(FlaskForm):
    """Sub-form for a single asset."""
    class Meta:
        csrf = False   # Disable CSRF for sub-forms

    name   = StringField("Asset Name",        default="Asset",
                         validators=[DataRequired()])
    mu     = FloatField("Expected Return (μ)", default=0.08,
                        validators=[DataRequired()])
    sigma  = FloatField("Volatility (σ)",      default=0.20,
                        validators=[DataRequired(), NumberRange(min=0.001)])
    weight = FloatField("Weight",              default=0.33,
                        validators=[DataRequired(), NumberRange(min=0.001, max=1.0)])


class PortfolioForm(FlaskForm):
    """Main portfolio simulation form."""
    initial_value  = FloatField("Initial Portfolio Value ($)",
                                default=100_000,
                                validators=[DataRequired(), NumberRange(min=1)])
    n_simulations  = IntegerField("Number of Simulations",
                                  default=1000,
                                  validators=[DataRequired(), NumberRange(min=100, max=10000)])
    n_days         = IntegerField("Simulation Days",
                                  default=252,
                                  validators=[DataRequired(), NumberRange(min=10, max=1260)])
    submit         = SubmitField("Run Simulation")


class MonteCarloForm(FlaskForm):
    """Random walk / stochastic process form."""
    mu            = FloatField("Drift (μ)",     default=0.05,
                               validators=[Optional()])
    sigma         = FloatField("Volatility (σ)", default=1.0,
                               validators=[DataRequired(), NumberRange(min=0.001)])
    n_steps       = IntegerField("Steps",         default=200,
                                 validators=[DataRequired(), NumberRange(min=10, max=2000)])
    n_paths       = IntegerField("Paths",          default=50,
                                 validators=[DataRequired(), NumberRange(min=1, max=500)])
    initial_value = FloatField("Initial Value",   default=100.0,
                               validators=[DataRequired(), NumberRange(min=0.01)])
    submit        = SubmitField("Simulate")