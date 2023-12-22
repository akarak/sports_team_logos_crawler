import json
from pydantic import BaseModel


class Task(BaseModel):
    url: str
    prefix: str


def load_task(filepath: str) -> Task:
    with open(filepath, mode="rt", encoding="utf-8") as f:
        data = json.load(f)
        return Task(**data)
