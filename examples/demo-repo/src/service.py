from json import loads


def normalize(value: str) -> str:
    return value.strip().lower()


def handle_request(payload: str) -> dict:
    data = loads(payload)
    return {"name": normalize(data["name"])}