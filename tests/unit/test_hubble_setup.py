import json

import httpx
import pytest

from pathlib import Path

from scripts.setup_hubble import (
    CONNECTIONS,
    MAX_HUBBLE_PASSWORD_LENGTH,
    connect_hubble,
    generate_password,
    rotate_local_admin,
)


@pytest.mark.parametrize("existing", [False, True])
def test_connects_existing_graph_without_reinitializing(existing):
    requests = []

    def handle(request):
        requests.append(request)
        if request.method == "GET":
            records = (
                [
                    {
                        "id": 7,
                        "name": "MyGraph",
                        "host": "hugegraph-server",
                        "port": 8080,
                        "graph": "hugegraph",
                    }
                ]
                if existing
                else []
            )
            return httpx.Response(200, json={"status": 200, "data": {"records": records}})
        body = json.loads(request.content)
        assert body["graph"] == "hugegraph"
        assert body["password"] == "test-password"
        assert body["name"] == ("MyGraph" if existing else "EOIP")
        return httpx.Response(200, json={"status": 200, "data": {"id": 7}})

    with httpx.Client(base_url="http://hubble:8088", transport=httpx.MockTransport(handle)) as client:
        assert connect_hubble(client, "http://hugegraph-server:8080", "test-password") == 7
    assert [request.method for request in requests] == ["GET", "PUT" if existing else "POST"]
    assert requests[-1].url.path == (f"{CONNECTIONS}/7" if existing else CONNECTIONS)


def test_rotates_real_admin_id_without_clearing_graph():
    requests = []
    new_password = generate_password()

    def handle(request):
        requests.append(request)
        if request.url.path.endswith("/users"):
            return httpx.Response(200, json={"users": [{"id": "-31:admin", "user_name": "admin"}]})
        if request.method == "PUT":
            assert json.loads(request.content) == {"user_name": "admin", "user_password": new_password}
        return httpx.Response(200, json={})

    with httpx.Client(base_url="http://graph", transport=httpx.MockTransport(handle)) as client:
        rotate_local_admin(client, new_password)
    assert [request.method for request in requests] == ["GET", "PUT", "GET"]
    assert requests[1].url.path.endswith("/users/-31:admin")
    assert requests[2].url.path.endswith("/schema/vertexlabels")


@pytest.mark.parametrize("weak", ["admin", "ADMIN", "short-password", "x" * 49])
def test_rotation_never_sets_admin_or_weak_or_too_long_password(weak):
    """FT-SEC-HUBBLE: rotate_local_admin never sends user_password == 'admin'."""
    def handle(request):  # pragma: no cover - must not be reached
        raise AssertionError("no request may be sent for a rejected password")

    with httpx.Client(base_url="http://graph", transport=httpx.MockTransport(handle)) as client:
        with pytest.raises(ValueError):
            rotate_local_admin(client, weak)


def test_generated_password_fits_hubble_and_has_192_bits():
    """FT-X04: generated password is <=48 chars with >=192 bits of entropy."""
    values = {generate_password() for _ in range(50)}
    assert len(values) == 50
    for value in values:
        assert len(value) == 48 <= MAX_HUBBLE_PASSWORD_LENGTH
        assert all(c in "0123456789abcdef" for c in value)  # 48 hex chars = 192 bits


def test_connect_rejects_password_longer_than_hubble_column_before_any_request():
    """FT-X04: clear error instead of Hubble's 400 'Value too long for column PASSWORD'."""
    def handle(request):  # pragma: no cover - must not be reached
        raise AssertionError("no request may be sent")

    with httpx.Client(base_url="http://hubble", transport=httpx.MockTransport(handle)) as client:
        with pytest.raises(ValueError, match="at most 48"):
            connect_hubble(client, "http://hugegraph-server:8080", "a" * 64)


def test_no_literal_admin_password_in_setup_or_container_scripts():
    root = Path(__file__).resolve().parents[2]
    setup = (root / "scripts" / "setup_hubble.py").read_text(encoding="utf-8")
    ps1 = (root / "scripts" / "container.ps1").read_text(encoding="utf-8")
    assert '"user_password": "admin"' not in setup
    assert 'auth=("admin", "admin")' not in setup
    assert "HUGEGRAPH_PASSWORD=admin" not in ps1
    assert "$password = New-RandomHex -ByteCount 24" in ps1
    sh = (root / "scripts" / "container.sh").read_text(encoding="utf-8")
    assert "PASSWORD=$(openssl rand -hex 24)" in sh


def test_hubble_authentication_errors_are_not_swallowed():
    def handle(request):
        if request.method == "GET":
            return httpx.Response(200, json={"status": 200, "data": {"records": []}})
        return httpx.Response(401, json={})

    with (
        httpx.Client(base_url="http://hubble", transport=httpx.MockTransport(handle)) as client,
        pytest.raises(httpx.HTTPStatusError),
    ):
        connect_hubble(client, "http://hugegraph-server:8080", "invalid")


def test_rejects_unrelated_graph_host():
    with httpx.Client() as client, pytest.raises(ValueError, match="Local Hubble"):
        connect_hubble(client, "http://another-server:8080", "test")


def test_hubble_application_error_inside_http_success_is_not_swallowed():
    def handle(request):
        return httpx.Response(200, json={"status": 400, "data": None})

    with (
        httpx.Client(base_url="http://hubble", transport=httpx.MockTransport(handle)) as client,
        pytest.raises(RuntimeError, match="application status 400"),
    ):
        connect_hubble(client, "http://hugegraph-server:8080", "test")
