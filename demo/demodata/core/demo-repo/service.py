"""EOIP-1: Trace requirements to a bounded impact calculation."""
import math


def normalize(value):
    return math.floor(value)


def compute_impact(value):
    return normalize(value)
