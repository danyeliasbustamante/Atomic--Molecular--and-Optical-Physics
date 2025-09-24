"""
AMOP: Active Matter Order Parameters (and simple simulations)

API principal expuesta:
- simulate_active_particles
- polarization
- nematic_order_2d
"""

from .simulate import simulate_active_particles
from .order_params import polarization, nematic_order_2d
from .bootstrap import get_rng, set_seed

__all__ = [
    "simulate_active_particles",
    "polarization",
    "nematic_order_2d",
    "get_rng",
    "set_seed",
]

__version__ = "0.1.0"
