import os, sys
sys.path.insert(0, "packages")
sys.path.insert(0, ".")
token = "test-token-1234567890-secure-deployment"
os.environ["EOIP_API_TOKEN"] = token
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
