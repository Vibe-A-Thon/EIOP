"""Packaging checks for the proprietary/third-party licensing boundary.

These assertions check files and metadata, not legal sufficiency or clearance.
"""

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNERS = "Avyukthi AI and Murthy Ravinder kumar"


def test_python_license_metadata_includes_every_policy_document():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert config["project"]["license"] == "LicenseRef-EOIP-Proprietary"
    included = {path.relative_to(ROOT).as_posix()
                for pattern in config["project"]["license-files"] for path in ROOT.glob(pattern)}
    assert {"LICENSE", "NOTICE", "LICENSING.md", "THIRD_PARTY_NOTICES.md",
            "licenses/COMMERCIAL-LICENSE-DRAFT.md", "licenses/ORDER-FORM-TEMPLATE.md",
            "licenses/THIRD-PARTY-POLICY.md", "licenses/OWNERSHIP-REGISTER.md",
            "licenses/RELEASE-CHECKLIST.md"} <= included


def test_first_party_notice_reserves_only_owned_rights():
    notice = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert notice.startswith("EOIP PROPRIETARY SOFTWARE NOTICE")
    assert OWNERS in notice
    assert "THIRD-PARTY RIGHTS ARE PRESERVED" in notice
    assert "does not revoke or replace rights validly granted" in notice
    assert "NO PUBLIC LICENSE GRANT" in notice


def test_module_manifests_do_not_offer_a_public_license():
    for app in ("web", "vscode-extension"):
        directory = ROOT / "apps" / app
        package = json.loads((directory / "package.json").read_text(encoding="utf-8"))
        lock = json.loads((directory / "package-lock.json").read_text(encoding="utf-8"))
        assert package["license"] == lock["packages"][""]["license"] == "UNLICENSED"
        assert OWNERS in (directory / "LICENSE").read_text(encoding="utf-8")


def test_browser_notice_matches_module_notice_and_is_packaged():
    web = ROOT / "apps/web"
    assert (web / "LICENSE").read_bytes() == (web / "public/legal/LICENSE").read_bytes()
    assert (web / "public/legal/NOTICE").is_file()
    assert "COPY public ./public" in (web / "Dockerfile").read_text(encoding="utf-8")


def test_release_review_is_not_misrepresented_as_clearance():
    checklist = (ROOT / "licenses/RELEASE-CHECKLIST.md").read_text(encoding="utf-8")
    assert "NOT CLEARED FOR COMMERCIAL DISTRIBUTION" in checklist
    assert "extract-msg" in checklist
    assert "[ ] Confirm legal entity/trading-name relationship" in checklist
    terms = (ROOT / "licenses/COMMERCIAL-LICENSE-DRAFT.md").read_text(encoding="utf-8")
    assert "NOT AN EXECUTED AGREEMENT" in terms
    assert "Hosted SaaS" in terms and "Customer-Installed Software" in terms


def test_api_image_copies_legal_documents_before_build():
    dockerfile = (ROOT / "deploy/Dockerfile").read_text(encoding="utf-8")
    build = dockerfile.index("RUN pip install --no-cache-dir --no-deps .")
    assert dockerfile.index("COPY LICENSE NOTICE LICENSING.md THIRD_PARTY_NOTICES.md ./") < build
    assert dockerfile.index("COPY licenses ./licenses") < build
