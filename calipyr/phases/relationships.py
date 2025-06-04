# calipyr/phases/relationships.py

def void_ratio_from_porosity(n):
    """Convert porosity (n) to void ratio (e)"""
    return n / (1 - n)


def porosity_from_void_ratio(e):
    """Convert void ratio (e) to porosity (n)"""
    return e / (1 + e)


def degree_of_saturation(w, Gs, e):
    """Compute degree of saturation Sr from water content (w), specific gravity (Gs), and void ratio (e)"""
    return (w * Gs) / e


def dry_density(Gs, e, rho_w=1000):
    """Calculate dry density (ρ_dry) from specific gravity (Gs), void ratio (e), and unit water density (rho_w)"""
    return (Gs * rho_w) / (1 + e)


# Add more as needed...


# Example usage:
# from calipyr.phases.relationships import void_ratio_from_porosity
# e = void_ratio_from_porosity(0.4)
# print(f"Void ratio is {e:.3f}")

calipyr / tests / test_phases.py
