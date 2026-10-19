# Shared Python Packages

The installable Python distribution is declared in [pyproject.toml](../pyproject.toml), using `packages/` as its source root and discovering `eoip*`. Install from repository root with `python -m pip install -e ".[dev]"` for development.

The [EOIP package map](eoip/README.md) identifies domain ownership. Applications in `apps/` compose these modules; browser code and deployment entry points are not separate installed Python distributions. Do not assume installing the wheel alone supplies all root-relative configuration, demo assets, application modules or deployment scripts needed for the full stack.

The new `packages/reva/` compatibility directory and root-level `reva/` implementation are outside the manifest's `eoip*` discovery filter. Consult the [REVA component guide](../reva/README.md) before assuming they are included in an installed distribution or share EOIP's dependency and data-root configuration.

Dependency locks and optional extras are different distribution profiles. Review [neural tiers](../docs/install-neural.md) and [licensing](../LICENSING.md) before changing packages. Keep core installation independent of optional numerical/model runtimes.
