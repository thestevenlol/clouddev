"""
Code borrowed from: https://james-ramsden.com/map-a-value-from-one-number-scale-to-another-formula-and-c-code/
"""

def map_value(a0, a1, b0, b1, a):
    return b0 + (b1 - b0) * ((a - a0) / (a1 - a0))