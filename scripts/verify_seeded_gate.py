import os, sys
sys.path.insert(0, "packages")
sys.path.insert(0, ".")

from eoip.graph.memory import MemoryGraphStore
from tests.unit.test_product_intelligence import _seed_runtime_facts
from apps.api.main import create_app as main_create_app
from fastapi.testclient import TestClient

# FT-AUTH: no default principal; provision a throwaway superadmin token for this local run.
import hashlib, secrets, tempfile  # noqa: E401
token = secrets.token_urlsafe(32)
_asg = os.path.join(tempfile.mkdtemp(prefix="eoip-gate-"), "asg")
with open(_asg, "w", encoding="utf-8") as _fh:
    _fh.write(f"sha256:{hashlib.sha256(token.encode()).hexdigest()} | superadmin | * | gate-check\n")
os.chmod(_asg, 0o400)
os.environ["EOIP_ASG_FILE"] = _asg
os.environ["EOIP_GRAPH_BACKEND"] = "memory"

# In production or runtime, seed the core schema/runtime facts
app = main_create_app()
# Get store from app state or test
store = app.state.store if hasattr(app.state, "store") else None
# If main_create_app holds store in lifespan or app, let's see
print("Has store:", store is not None)

from eoip.product.intelligence import build_product_capability_report
from pathlib import Path
routes = {str(getattr(r, "path", "")) for r in app.routes if getattr(r, "path", None)}
store = MemoryGraphStore()
_seed_runtime_facts(store)
report = build_product_capability_report(repo_root=Path.cwd(), store=store, available_routes=routes)
print("Score:", report["enterprise_grade_score"])
print("First Choice Gate:", report["first_choice_gate"])
print("Advanced Ready Count:", report["advanced_ready_count"], "/", report["capability_count"])
