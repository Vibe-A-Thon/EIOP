# EOIP Research Datasets Notice

This directory contains research reference datasets:
1. `competitive-research-matrix.csv`
2. `ontology-comparison-matrix.csv`
3. Held-out benchmark datasets

These are dataset categories referenced by the research programme, not a guarantee that each dataset is physically present in this directory. Locate the actual versioned artifact and provenance before running an analysis; never fabricate a missing holdout dataset or silently substitute training data.

## Binding Separation Notice (CRA-042, X-26)

**DO NOT MERGE THESE DATASETS.**
The competitive matrix and ontology comparison matrix reflect distinct research methodologies, scopes, and scoring semantics. Merging, averaging, or reconciling their scores into a single monolithic score is strictly prohibited. Unqualified and ND (Not Determined) scores must be preserved as distinct states and never coerced to zero or interpolated.

## Reproducibility

Record source version/hash, provenance, permitted use, sampling, preprocessing, splits and missing-value handling. Keep holdout data separate from model/prompt tuning. Report measurements as dataset/profile-specific and retain uncertainty. See the [research overview](../README.md), [benchmark guide](../../benchmarks/README.md) and [evidence rules](../../docs/testing-guide.md).
