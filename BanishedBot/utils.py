from asyncio import Lock

class LockingCache(Lock):
    def __init__(self) -> None:
        self.cache = {}
        super().__init__()