from asyncio import Lock

class LockingCache(Lock):
    def __init__(self) -> None:
        super().__init__()
        self.cache = {}