"""Tenant-configurable ordering for the shared IP Warrant status enum."""

from __future__ import annotations

from collections.abc import Sequence

from eoip.contracts.warrant import WarrantStatus

DEFAULT_WARRANT_STATUS_ORDER = (
    WarrantStatus.OBSERVED,
    WarrantStatus.ATTESTED,
    WarrantStatus.PREDICTED,
    WarrantStatus.GENERATED,
    WarrantStatus.HEARSAY,
    WarrantStatus.UNKNOWN,
)
ALLOWED_WARRANT_STATUS_ORDERS = frozenset({
    DEFAULT_WARRANT_STATUS_ORDER,
    (
        WarrantStatus.ATTESTED,
        WarrantStatus.OBSERVED,
        WarrantStatus.PREDICTED,
        WarrantStatus.GENERATED,
        WarrantStatus.HEARSAY,
        WarrantStatus.UNKNOWN,
    ),
})


def validate_warrant_status_order(values: Sequence[str | WarrantStatus]) -> tuple[WarrantStatus, ...]:
    """Accept the default order or its sole permitted top-pair swap."""

    try:
        order = tuple(value if isinstance(value, WarrantStatus) else WarrantStatus(value) for value in values)
    except (TypeError, ValueError) as exc:
        raise ValueError("WAR_INVALID_ORDER") from exc
    if len(order) != len(WarrantStatus) or len(set(order)) != len(WarrantStatus):
        raise ValueError("WAR_INVALID_ORDER")
    if order not in ALLOWED_WARRANT_STATUS_ORDERS:
        raise ValueError("WAR_INVALID_ORDER")
    return order


def warrant_status_rank(
    status: str | WarrantStatus,
    *,
    order: Sequence[str | WarrantStatus] = DEFAULT_WARRANT_STATUS_ORDER,
) -> int:
    """Return zero for the highest status under a validated tenant order."""

    normalized_order = validate_warrant_status_order(order)
    try:
        normalized_status = status if isinstance(status, WarrantStatus) else WarrantStatus(status)
    except (TypeError, ValueError) as exc:
        raise ValueError("Unknown warrant status") from exc
    return normalized_order.index(normalized_status)


def minimum_warrant_status(
    statuses: Sequence[str | WarrantStatus],
    *,
    order: Sequence[str | WarrantStatus] = DEFAULT_WARRANT_STATUS_ORDER,
) -> WarrantStatus:
    """Return the weakest status; an empty input set is UNKNOWN."""

    normalized_order = validate_warrant_status_order(order)
    if not statuses:
        return WarrantStatus.UNKNOWN
    normalized_statuses = []
    for status in statuses:
        try:
            normalized_statuses.append(
                status if isinstance(status, WarrantStatus) else WarrantStatus(status)
            )
        except (TypeError, ValueError) as exc:
            raise ValueError("Unknown warrant status") from exc
    return max(normalized_statuses, key=normalized_order.index)