from typing import Any


class Pagination:
    def __init__(self, page: int = 1, size: int = 10):
        self.page = max(1, page)
        self.size = max(1, min(100, size))

    def offset(self) -> int:
        return (self.page - 1) * self.size

    def limit(self) -> int:
        return self.size
