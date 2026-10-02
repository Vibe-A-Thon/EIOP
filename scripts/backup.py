import argparse
from datetime import UTC, datetime

from eoip.runtime import create_store, data_root
from eoip.snapshot import backup

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export a quiescent EOIP graph and raw evidence")
    parser.add_argument("--output")
    args = parser.parse_args()
    destination = args.output or str(
        data_root() / "backups" / f"eoip-{datetime.now(UTC):%Y%m%dT%H%M%SZ}.json"
    )
    store = create_store()
    try:
        print(backup(store, data_root(), destination))
    finally:
        store.close()
