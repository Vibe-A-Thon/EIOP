# ADR-H16 — CUDA packages are not redistributed

| Field | Value |
|---|---|
| Decision | H-16 (CRAr_cpccaggcc-requirements.md, section 18.2) |
| Status | **Accepted — 2026-10-18** |
| Decided by | Ravaleedhar Reddy: "it is not possible to redistribute CUDA Packages" (2026-10-18) |
| Governs | CRA-043.2, CRA-043.3, CRA-035.9, section 13 licensing rows |
| Related | ADR-H15 (CPU-first stack), ADR-H17 (GPU availability, open) |

## Context

CUDA-enabled torch wheels depend on `nvidia-*` packages distributed under the NVIDIA Software License Agreement, which is not an open-source license and restricts redistribution. EOIP ships wheels, offline (air-gap) wheel bundles and container images, all of which count as distribution.

## Decision

1. No `nvidia-*` package, CUDA runtime library or CUDA-enabled torch build is included in any artifact EOIP distributes: wheels, lock files used for distribution, offline wheel bundles, container images, appliances, mirrors or download sites.
2. EOIP distributes CPU-only torch builds (ADR-H15).
3. A customer may, at their own discretion and under their own acceptance of NVIDIA's terms, install a CUDA build obtained directly from upstream into their own environment. EOIP may detect it at runtime. That path is customer-provisioned, unqualified until ADR-H17, and never required by any EOIP capability or gate.

## Not decided here

Whether EOIP may operate GPUs in infrastructure it runs itself (SaaS) is folded into ADR-H17. If that is pursued, Legal confirms the position separately.

## Consequences

- The CI license gate rejects any `nvidia-*` package in a distributed artifact without exception (CRA-035.9). Bundle manifests and image SBOMs are scanned for it (CRA-043.3).
- EOIP documentation describes CPU installation only. Customer-provisioned GPU installation is described as unsupported until ADR-H17, with upstream links and no EOIP-hosted packages.
- Risk NR15 in the Graph-Neurons plan is closed by this decision.
