"""Run existing browser checks on an owned loopback-only Vite server."""

import argparse
import os
import shutil
import socket
import subprocess
import time
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    root = Path.cwd()
    app = root / "apps/web"
    node = shutil.which("node")
    if not node:
        raise SystemExit("Node unavailable")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    url = f"http://127.0.0.1:{port}"
    args.out.mkdir(parents=True, exist_ok=True)
    server = subprocess.Popen([node, str(app / "node_modules/vite/bin/vite.js"),
                               "--host", "127.0.0.1", "--port", str(port), "--strictPort"],
                              cwd=app, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(120):
            if server.poll() is not None:
                raise RuntimeError("Owned Vite server exited before readiness")
            try:
                with urllib.request.urlopen(url, timeout=1) as response:
                    if response.status == 200:
                        break
            except OSError:
                time.sleep(.25)
        else:
            raise RuntimeError("Owned Vite server readiness timed out")
        env = dict(os.environ, PLAYWRIGHT_BASE_URL=url, EOIP_GUI_WEB_SERVER="0",
                   PLAYWRIGHT_JSON_OUTPUT_FILE=str(args.out / "playwright.json"))
        result = subprocess.run([node, str(app / "node_modules/@playwright/test/cli.js"), "test",
                                 "tests/gui-foundations.spec.js", "tests/gui-accessibility.spec.js",
                                 "tests/gui-graph-contracts.spec.js", "tests/qa-nonfunctional.spec.js",
                                 "--reporter=list,json", "--workers=1", "--max-failures=10",
                                 "--output=" + str(args.out / "test-results")],
                                cwd=app, env=env, timeout=600, check=False)
        return result.returncode
    finally:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(server.pid), "/T", "/F"],
                           capture_output=True, check=False)
        else:
            server.terminate()
        server.wait(timeout=20)


if __name__ == "__main__":
    raise SystemExit(main())
