import os, sys
sys.path.insert(0, "packages")
sys.path.insert(0, ".")
# FT-AUTH: no default principal; provision a throwaway superadmin token for this local run.
import hashlib, secrets, tempfile  # noqa: E401
token = secrets.token_urlsafe(32)
_asg = os.path.join(tempfile.mkdtemp(prefix="eoip-gate-"), "asg")
with open(_asg, "w", encoding="utf-8") as _fh:
    _fh.write(f"sha256:{hashlib.sha256(token.encode()).hexdigest()} | superadmin | * | gate-check\n")
os.chmod(_asg, 0o400)
os.environ["EOIP_ASG_FILE"] = _asg
os.environ["EOIP_GRAPH_BACKEND"] = "memory"

from apps.api.main import create_app as main_create_app
from fastapi.testclient import TestClient

app = main_create_app()
client = TestClient(app)
resp = client.get('/api/v1/product/capabilities', headers={"Authorization": f"Bearer {token}"})
data = resp.json()

for cap in data.get('capabilities', []):
    print(f"=== {cap['capability_id']}: {cap['name']} ({cap['priority']}) - {cap['status']} (score {cap['score']}) ===")
    for check in cap['checks']:
        if not check.get('present'):
            print(f"   MISSING: kind={check['kind']} target={check['target']} error={check.get('error')}")
