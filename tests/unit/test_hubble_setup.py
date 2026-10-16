import json

import httpx
import pytest

from scripts.setup_hubble import CONNECTIONS, connect_hubble, rotate_local_admin


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

    def handle(request):
        requests.append(request)
        if request.url.path.endswith("/users"):
            return httpx.Response(200, json={"users": [{"id": "-31:admin", "user_name": "admin"}]})
        if request.method == "PUT":
            assert json.loads(request.content) == {"user_name": "admin", "user_password": "admin"}
        return httpx.Response(200, json={})

    with httpx.Client(base_url="http://graph", transport=httpx.MockTransport(handle)) as client:
        rotate_local_admin(client)
    assert [request.method for request in requests] == ["GET", "PUT", "GET"]
    assert requests[1].url.path.endswith("/users/-31:admin")
    assert requests[2].url.path.endswith("/schema/vertexlabels")


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
