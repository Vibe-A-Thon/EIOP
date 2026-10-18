# Optional Neural Tiers

EOIP core does not require NumPy, SciPy, scikit-learn, PyTorch, or PyTorch Geometric. The numerical stack is opt-in so core installs remain suitable for air-gapped and edge deployments.

## N0: Numerics

Install the CPU numerical foundation from the repository root:

```powershell
python -m pip install -e ".[numerics]"
```

This installs the `numerics` extra declared in `pyproject.toml`: NumPy, SciPy, and scikit-learn. It does not install Torch or GPU/CUDA packages.

For the locked core-plus-N0 environment:

```powershell
python -m pip install --require-hashes -r requirements-neural.lock
```

The lock was generated from `pyproject.toml` with `pip-compile --extra numerics --generate-hashes`. It pins the resolver output, including the core project dependencies and N0 packages. Rebuild it after dependency or project metadata changes, then run `tests/compliance/test_no_cuda_packages.py`.

## Higher Tiers

N1 (Torch/PyG), N2 (local text models), and N3 (research packages) are not yet declared or qualified in this checkout. Do not interpret their runtime enums or existing experimental modules as installable or production-ready capabilities. Until their extras, CPU-only package source, license inventory, tier-matrix tests, and model qualification are complete, inference entry points fail closed when the neural tier is missing or no model has passed promotion gates.

## Current Qualification Boundary

N0 was installed and tested on Windows x86_64 with Python 3.11.9. The `100,000 x 128` cosine benchmark measured above the specified 20 ms target on this host; the result is a performance failure for this profile, not a passed target. Offline wheel-bundle installation, Linux matrix runs, and N1–N3 are not qualified. The exact N0 wheel notices, including bundled native-library terms, are listed in `THIRD_PARTY_NOTICES.md`; commercial distribution remains subject to the repository's license review gate.
