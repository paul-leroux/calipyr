# material.py
# Constitutive functions for NorSand model
import numpy as np

def compute_gmax(e, p):
    """Elastic shear modulus."""
    return 100 * p / (1 + e)

def compute_ec(n, lambda_, p, pref=100.0):
    """Critical state void ratio."""
    return n - lambda_ * np.log(p / pref)

def compute_yield_function(q, p, psi, pimg, mc, n):
    """NorSand yield surface."""
    mpsi = mc * (1 - n * psi)
    return q / p - mpsi * (1 - p / pimg)

def compute_mpsi(mc, n, psi):
    return mc * (1 - n * psi)