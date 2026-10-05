"""Connect Hubble to the existing graph; optionally enable local demo credentials."""

import argparse
import os
from urllib.parse import quote, urlparse

import httpx

CONNECTIONS = "/api/v1.2/graph-connections"


def hubble_data(response: httpx.Response) -> dict:
    response.raise_for_status()
    body = response.json()
    if body["status"] != 200:
        raise RuntimeError(f"Hubble operation failed (application status {body['status']})")
    return body["data"]


def rotate_local_admin(client: httpx.Client) -> None:
    response = client.get("/graphspaces/DEFAULT/auth/users")
    response.raise_for_status()
    users = [user for user in response.json()["users"] if user["user_name"] == "admin"]
    if len(users) != 1:
        raise RuntimeError("Expected exactly one existing HugeGraph admin account")
    user_id = quote(str(users[0]["id"]), safe="")
    response = client.put(
        f"/graphspaces/DEFAULT/auth/users/{user_id}",
        json={"user_name": "admin", "user_password": "admin"},
    )
    response.raise_for_status()
    response = client.get(
        "/graphspaces/DEFAULT/graphs/hugegraph/schema/vertexlabels",
        auth=("admin", "admin"),
    )
    response.raise_for_status()


def connect_hubble(client: httpx.Client, graph_url: str, password: str) -> int:
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
        with httpx.Client(
            base_url=graph_url, auth=("admin", password), timeout=120, trust_env=False
        ) as client:
            rotate_local_admin(client)
        print("Existing admin credential updated; graph data and schema retained.")
    else:
        with httpx.Client(base_url="http://hubble:8088", timeout=120, trust_env=False) as client:
            connection_id = connect_hubble(client, graph_url, password)
        print(f"Hubble connection {connection_id} ready: existing DEFAULT/hugegraph.")


if __name__ == "__main__":
    main()
