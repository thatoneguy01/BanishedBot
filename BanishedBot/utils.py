from asyncio import Lock
import json

import sqlalchemy.types as types


class LockingCache(Lock):
    def __init__(self) -> None:
        self.cache = {}
        super().__init__()


class Json(types.TypeDecorator):
    @property
    def python_type(self):
        return object

    impl = types.String

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_literal_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None
