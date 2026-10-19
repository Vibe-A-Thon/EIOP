"""
Unit Tests for Module RO: Headless Browser CDP, DOM Sanitization, and Interaction Recording (T-ENH-029..031).
"""

import pytest

from reva.obs.browser_cdp import CDPController
from reva.obs.dom_harvester import DOMHarvester
from reva.obs.interaction_recorder import InteractionRecorder
from reva.core.errors import RevaSecurityError


def test_cdp_controller_domain_fencing():
    controller = CDPController(allowed_domains=["127.0.0.1", "localhost", "app.local"])

    # Permitted local navigation
    cmd = controller.build_navigate_command("http://127.0.0.1:8000/dashboard")
    assert cmd.method == "Page.navigate"
    assert cmd.params["url"] == "http://127.0.0.1:8000/dashboard"

    # Blocked external navigation
    with pytest.raises(RevaSecurityError):
        controller.build_navigate_command("https://evil-exfiltration-site.com/steal")


def test_dom_harvester_sanitization():
    harvester = DOMHarvester()

    raw_html = """
    <html>
      <body>
        <form>
          <input type="text" name="username" value="admin_user">
          <input type="password" name="pwd" value="SuperSecretP@ssword123">
        </form>
      </body>
    </html>
    """
    snapshot = harvester.sanitize_html_dom(raw_html, "http://localhost:8000/login")
    assert snapshot.redactions_count == 1
    assert "SuperSecretP@ssword123" not in snapshot.html_content
    assert "[REDACTED_PASSWORD]" in snapshot.html_content
    assert "admin_user" in snapshot.html_content

    # Header scrubbing
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer secret_jwt_token_12345",
        "Cookie": "session_id=abcxyz987",
    }
    scrubbed = harvester.sanitize_headers(headers)
    assert scrubbed["Content-Type"] == "application/json"
    assert scrubbed["Authorization"] == "[REDACTED_HEADER]"
    assert scrubbed["Cookie"] == "[REDACTED_HEADER]"


def test_interaction_recorder_and_warrant():
    recorder = InteractionRecorder("sess_101", "http://localhost:8000/test")
    recorder.record_action("CLICK", "#submit-button")
    recorder.record_action("TYPE", "#input-name", "Test User")

    session_rec = recorder.finalize_session()
    assert len(session_rec.actions) == 2
    assert session_rec.warrant_id.startswith("wr1_")
    assert session_rec.actions[0].action_type == "CLICK"
