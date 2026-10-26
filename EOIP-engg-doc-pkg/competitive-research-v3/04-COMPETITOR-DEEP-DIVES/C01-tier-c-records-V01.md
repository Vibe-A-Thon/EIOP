# C01 — Tier C records (batch V01)

Verified on 2026-10-26. Worker V01. Parent deep dive: `C01-falkordb.md`.

### T-C01-redisgraph — RedisGraph (historical)

| Field | Value |
|---|---|
| Official URL | https://github.com/RedisGraph/RedisGraph ; EOL notice https://redis.io/blog/redisgraph-eol/ |
| Owner | Redis Ltd. |
| Latest version + date | NOT PUBLICLY VERIFIED from sources read (releases section empty in the capture; Redis Software release notes list bundled v2.10) |
| Status | End-of-life. End of sale 2023-07-05; end of support 2025-01-31; GitHub in maintenance mode, patches considered only until 2024-12-31, to be tagged deprecated 2025-02-01; README: "no longer maintained" |
| Licence + class | Choose one of RSALv2, SSPLv1, AGPLv3 (source-available / network-copyleft mix) |
| Deployment modes | Redis module; formerly Redis Stack (removed from 7.2.x) and Redis Enterprise |
| Air-gap viable | Yes technically, but unmaintained; no RESP3 support was planned |
| Tier reason | End-of-life; lessons only |

**Relevance.** RedisGraph is a Redis module that implemented a property graph with openCypher using GraphBLAS sparse matrices. Redis ended it because graph adoption needed heavy pre- and post-sales investment (steep learning curve, long PoCs, low success rate) relative to Redis Search, JSON and Vector; its own words concede the graph offering was "technically competitive" but the cost to scale capacity was higher than anticipated [CLAIM-redisgraph-01]. Lessons for EOIP: (1) a graph engine embedded in another product's process and licence inherits that parent's strategy risk, so EOIP's `GraphStore` abstraction (BL-01) should never make a single vendor-module backend a hard dependency; (2) licence choice (RSALv2/SSPLv1/AGPLv3) did not prevent abandonment, and the community successor is FalkorDB, itself SSPL-licensed, see `C01-falkordb.md`; (3) customers asked for migration paths: FalkorDB reads RedisGraph RDB files [CLAIM-redisgraph-02], a design to copy for EOIP import/export (CAP-22 not relevant; touches CAP-01, CAP-77, CAP-14).

**Decision.** REFERENCE-ONLY. Do not build an adapter; point legacy RedisGraph users to the FalkorDB path.

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-redisgraph-01 | RedisGraph, EOL | EOL announced 2023-07-05; end of support 2025-01-31; maintenance mode; deprecated tag 2025-02-01; not in Redis Stack from 7.2.x; RESP3 not planned; motivations as stated; licence RSALv2 or SSPLv1 | Officially documented | Redis blog "RedisGraph EOL", redis.io/blog/redisgraph-eol/ | 2023-07-05 (updated 2026-06-01) / 2026-10-26 | 0.95 | none |
| CLAIM-redisgraph-02 | repo + FalkorDB docs | Repo README states "no longer maintained"; licence choice of RSALv2/SSPLv1/AGPLv3; FalkorDB is the successor and reads RedisGraph RDB | Officially documented | github.com/RedisGraph/RedisGraph ; docs.falkordb.com/operations/migration/redisgraph-to-falkordb.md | 2026-10-26 | 0.85 | latest tag not retrievable |
