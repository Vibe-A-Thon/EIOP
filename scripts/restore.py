import argparse

from eoip.runtime import create_store, data_root
from eoip.snapshot import restore

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restore into an empty, isolated EOIP deployment")
    parser.add_argument("source")
    args = parser.parse_args()
    store = create_store()
    try:
        print(restore(store, data_root(), args.source))
    finally:
        store.close()
