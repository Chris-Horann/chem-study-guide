from collections import Counter
from chempy import balance_stoichiometry
from periodictable import formula
from pint import UnitRegistry

ureg = UnitRegistry()


def molar_mass(formula_text: str) -> float:
    """Return molar mass in g/mol."""
    return float(formula(formula_text).mass)


def balance_reaction(reactants: list[str], products: list[str]):
    """Return balanced stoichiometric coefficients using ChemPy."""
    reac, prod = balance_stoichiometry(set(reactants), set(products))
    return dict(reac), dict(prod)


def check_unit_conversion(value, from_unit: str, to_unit: str):
    """Convert a numerical value between compatible units."""
    quantity = value * ureg(from_unit)
    return quantity.to(to_unit)


if __name__ == "__main__":
    print("ChemStudy chemistry verification helper loaded.")
    print("Examples:")
    print("  molar_mass('H2O')")
    print("  balance_reaction(['H2', 'O2'], ['H2O'])")
    print("  check_unit_conversion(1000, 'mL', 'L')")
