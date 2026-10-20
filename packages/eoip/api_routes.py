"""Effective route enumeration across FastAPI versions (FT-D04).

FastAPI >= 0.142 keeps ``include_router`` lazy: ``app.routes`` holds an
``_IncludedRouter`` per nested include instead of the flattened routes, so code
that read ``route.path`` from ``app.routes`` silently missed every route mounted
through a nested router (for example ``/api/v1/loops/catalog`` via the extended
router). This walks those wrappers and yields the effective routes.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any


def iter_effective_routes(routes: Iterable[Any]) -> Iterator[Any]:
    for route in routes:
        candidates = getattr(route, "effective_candidates", None)
        if callable(candidates) and not hasattr(route, "path"):
            yield from iter_effective_routes(candidates())
        else:
            yield route


def route_paths(app: Any) -> set[str]:
    return {str(route.path) for route in iter_effective_routes(app.routes) if getattr(route, "path", None)}
