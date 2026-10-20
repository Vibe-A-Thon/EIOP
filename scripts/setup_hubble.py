"""Connect Hubble to the existing graph; optionally rotate the local graph admin password.

FT-X04: Hubble stores the connection password in a VARCHAR(48) column, so graph
passwords used for the Hubble connection must be at most 48 characters.
FT-SEC-HUBBLE: ``--rotate-local-admin`` sets a fresh CSPRNG password supplied in
``EOIP_HUGEGRAPH_NEW_PASSWORD`` (never the well-known ``admin``) and never prints it.
"""

import argparse
import os
import secrets
from urllib.parse import quote, urlparse

import httpx

CONNECTIONS = "/api/v1.2/graph-connections"
MAX_HUBBLE_PASSWORD_LENGTH = 48  # Hubble graph_connection.password is VARCHAR(48)
MIN_ROTATED_PASSWORD_LENGTH = 24
WELL_KNOWN_PASSWORDS = frozenset({"admin", "password", "hugegraph", "changeme", "pa"})


def generate_password() -> str:
    """192-bit CSPRNG password that fits Hubble's 48-character column."""
    return secrets.token_hex(24)


def validate_hubble_password(password: str) -> None:
    if not password:
        raise ValueError("HugeGraph password is empty")
    if len(password) > MAX_HUBBLE_PASSWORD_LENGTH:
        raise ValueError(
            f"HugeGraph password is {len(password)} characters; Hubble accepts at most "
            f"{MAX_HUBBLE_PASSWORD_LENGTH}. Rotate it with `scripts/container.ps1 hubble-local-admin` "
            "(or set a <=48 character HUGEGRAPH_PASSWORD in deploy/.env before the first start)"
        )


def hubble_data(response: httpx.Response) -> dict:
    response.raise_for_status()
    body = response.json()
    if body["status"] != 200:
        raise RuntimeError(f"Hubble operation failed (application status {body['status']})")
    return body["data"]


def rotate_local_admin(client: httpx.Client, new_password: str) -> None:
    """Set the existing graph 'admin' account to ``new_password`` (random, never 'admin')."""
    if new_password.lower() in WELL_KNOWN_PASSWORDS or len(new_password) < MIN_ROTATED_PASSWORD_LENGTH:
        raise ValueError(
            f"Refusing a well-known or short graph admin password (minimum {MIN_ROTATED_PASSWORD_LENGTH} characters)"
        )
    validate_hubble_password(new_password)
    response = client.get("/graphspaces/DEFAULT/auth/users")
    response.raise_for_status()
    users = [user for user in response.json()["users"] if user["user_name"] == "admin"]
    if len(users) != 1:
        raise RuntimeError("Expected exactly one existing HugeGraph admin account")
    user_id = quote(str(users[0]["id"]), safe="")
    response = client.put(
        f"/graphspaces/DEFAULT/auth/users/{user_id}",
        json={"user_name": "admin", "user_password": new_password},
    )
    response.raise_for_status()
    response = client.get(
        "/graphspaces/DEFAULT/graphs/hugegraph/schema/vertexlabels",
        auth=("admin", new_password),
    )
    response.raise_for_status()


def connect_hubble(client: httpx.Client, graph_url: str, password: str) -> int:
    validate_hubble_password(password)
    address = urlparse(graph_url)
    if address.scheme != "http" or address.hostname != "hugegraph-server" or address.port != 8080:
        raise ValueError("Local Hubble must connect to http://hugegraph-server:8080")
    response = client.get(CONNECTIONS, params={"page_size": 100})
    matches = [
        record
        for record in hubble_data(response)["records"]
        if record["host"] == address.hostname
        and record["port"] == address.port
        and record["graph"] == "hugegraph"
    ]
    if len(matches) > 1:
        raise RuntimeError("Multiple Hubble connections reference the local graph")
    body = {
        "name": "EOIP",
        "graph": "hugegraph",
        "host": address.hostname,
        "port": address.port,
        "username": "admin",
        "password": password,
    }
    if matches:
        body["id"] = matches[0]["id"]
        body["name"] = matches[0]["name"]
        response = client.put(f"{CONNECTIONS}/{body['id']}", json=body)
    else:
        response = client.post(CONNECTIONS, json=body)
    return int(hubble_data(response)["id"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rotate-local-admin", action="store_true")
    args = parser.parse_args()
    graph_url = os.environ["EOIP_HUGEGRAPH_URL"]
    password = os.environ["EOIP_HUGEGRAPH_PASSWORD"]
    if args.rotate_local_admin:
        new_password = os.environ.get("EOIP_HUGEGRAPH_NEW_PASSWORD", "")
        if not new_password:
            raise SystemExit("EOIP_HUGEGRAPH_NEW_PASSWORD is required (scripts/container.ps1 generates it)")
        with httpx.Client(
            base_url=graph_url, auth=("admin", password), timeout=120, trust_env=False
        ) as client:
            rotate_local_admin(client, new_password)
        print("Graph admin password rotated to a new random value (not printed); graph data and schema retained.")
    else:
        with httpx.Client(base_url="http://hubble:8088", timeout=120, trust_env=False) as client:
            connection_id = connect_hubble(client, graph_url, password)
        print(f"Hubble connection {connection_id} ready: existing DEFAULT/hugegraph.")


if __name__ == "__main__":
    main()
