"""Tests for the universal OCI container-runtime discovery layer."""

from __future__ import annotations

import json
import subprocess
from unittest.mock import patch, MagicMock

import pytest

from eoip.enterprise.container_runtime import (
    ContainerRuntime,
    ComposeInfo,
    discover,
    discover_all,
    require,
    _extract_version,
    _runtime_capabilities,
)


@pytest.mark.enterprise
class TestVersionExtraction:
    def test_semver(self):
        assert _extract_version("Docker version 27.5.1, build abcdef") == "27.5.1"

    def test_podman_version(self):
        assert _extract_version("podman version 5.3.1") == "5.3.1"

    def test_v_prefix(self):
        assert _extract_version("nerdctl v2.0.3") == "2.0.3"

    def test_no_digits(self):
        result = _extract_version("unknown tool")
        assert len(result) > 0


@pytest.mark.enterprise
class TestRuntimeCapabilities:
    def test_docker_full_caps(self):
        init, secopt, capdrop = _runtime_capabilities("docker")
        assert init and secopt and capdrop

    def test_podman_full_caps(self):
        init, secopt, capdrop = _runtime_capabilities("podman")
        assert init and secopt and capdrop

    def test_nerdctl_partial_caps(self):
        init, secopt, capdrop = _runtime_capabilities("nerdctl")
        assert init and not secopt and capdrop

    def test_unknown_no_caps(self):
        init, secopt, capdrop = _runtime_capabilities("unknown-runtime")
        assert not init and not secopt and not capdrop


@pytest.mark.enterprise
class TestDiscover:
    @patch("eoip.enterprise.container_runtime.shutil.which", return_value=None)
    def test_no_runtimes_returns_none(self, _which):
        assert discover() is None

    @patch("eoip.enterprise.container_runtime._detect_rootless", return_value=False)
    @patch("eoip.enterprise.container_runtime._probe_compose", return_value=None)
    @patch("eoip.enterprise.container_runtime._run_quiet")
    @patch("eoip.enterprise.container_runtime.shutil.which")
    def test_docker_discovered(self, mock_which, mock_run, _compose, _rootless):
        mock_which.side_effect = lambda x: "/usr/bin/docker" if x == "docker" else None
        mock_run.return_value = "Docker version 27.5.1, build abcdef"
        rt = discover()
        assert rt is not None
        assert rt.name == "docker"
        assert rt.version == "27.5.1"

    @patch("eoip.enterprise.container_runtime._detect_rootless", return_value=True)
    @patch("eoip.enterprise.container_runtime._probe_compose")
    @patch("eoip.enterprise.container_runtime._run_quiet")
    @patch("eoip.enterprise.container_runtime.shutil.which")
    def test_podman_preferred_via_env(self, mock_which, mock_run, mock_compose, _rootless):
        mock_which.side_effect = lambda x: f"/usr/bin/{x}" if x in ("docker", "podman") else None
        mock_run.return_value = "podman version 5.3.1"
        mock_compose.return_value = ComposeInfo(command=("podman", "compose"), version="1.2.0")
        rt = discover(preferred="podman")
        assert rt is not None
        assert rt.name == "podman"
        assert rt.rootless is True
        assert rt.compose is not None

    @patch("eoip.enterprise.container_runtime._detect_rootless", return_value=False)
    @patch("eoip.enterprise.container_runtime._probe_compose", return_value=None)
    @patch("eoip.enterprise.container_runtime._run_quiet")
    @patch("eoip.enterprise.container_runtime.shutil.which")
    def test_discover_all_finds_multiple(self, mock_which, mock_run, _compose, _rootless):
        found = {"docker", "podman"}
        mock_which.side_effect = lambda x: f"/usr/bin/{x}" if x in found else None
        mock_run.return_value = "version 1.0.0"
        runtimes = discover_all()
        names = {r.name for r in runtimes}
        assert "docker" in names
        assert "podman" in names


@pytest.mark.enterprise
class TestRequire:
    @patch("eoip.enterprise.container_runtime.discover", return_value=None)
    def test_raises_on_missing(self, _discover):
        with pytest.raises(EnvironmentError, match="No OCI container runtime"):
            require()

    @patch("eoip.enterprise.container_runtime.discover")
    def test_returns_runtime(self, mock_discover):
        rt = ContainerRuntime(
            name="docker", cli="docker", version="27.5.1",
            compose=None, rootless=False,
            supports_init=True, supports_security_opt=True, supports_cap_drop=True,
        )
        mock_discover.return_value = rt
        assert require() is rt


@pytest.mark.enterprise
class TestContainerRuntimeDataclass:
    def test_frozen(self):
        rt = ContainerRuntime(
            name="podman", cli="podman", version="5.3.1",
            compose=ComposeInfo(command=("podman", "compose"), version="1.2.0"),
            rootless=True,
            supports_init=True, supports_security_opt=True, supports_cap_drop=True,
        )
        with pytest.raises(AttributeError):
            rt.name = "docker"  # type: ignore[misc]

    def test_compose_info_frozen(self):
        ci = ComposeInfo(command=("docker", "compose"), version="2.32.0")
        with pytest.raises(AttributeError):
            ci.version = "3.0.0"  # type: ignore[misc]
