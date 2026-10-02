# EOIP-1 requirement trace

`service.py` implements EOIP-1. `compute_impact` calls `normalize`, which uses
the Python math module. EOIP-2 requires the path to retain source evidence.
