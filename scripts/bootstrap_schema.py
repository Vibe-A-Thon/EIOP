from eoip.runtime import create_store

if __name__ == "__main__":
    store = create_store()
    try:
        print(store.ensure_schema())
    finally:
        store.close()
