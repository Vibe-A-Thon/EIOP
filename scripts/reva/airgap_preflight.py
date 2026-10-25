#!/usr/bin/env python3
"""Prove the current process has no network (REVA-NFR-014 air-gap lane preflight).

Exits 0 only if outbound TCP to public addresses and DNS resolution both fail while loopback
works; otherwise exits 1, so the air-gap lane can never pass with the network still on.
"""

import socket
import sys


def can_connect(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except OSError:
        return False


def main() -> int:
    problems = []
    for host, port in (("1.1.1.1", 443), ("8.8.8.8", 53), ("140.82.112.3", 443)):
        if can_connect(host, port):
            problems.append(f"outbound TCP to {host}:{port} succeeded")
    try:
        socket.getaddrinfo("github.com", 443)
        problems.append("DNS resolution of github.com succeeded")
    except OSError:
        pass
    server = socket.socket()
    try:
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        if not can_connect("127.0.0.1", server.getsockname()[1]):
            problems.append("loopback is not usable (bring lo up)")
    finally:
        server.close()
    for problem in problems:
        print(f"::error::air-gap preflight: {problem}")
    if not problems:
        print("air-gap preflight: PASS (no outbound network, no DNS, loopback up)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
