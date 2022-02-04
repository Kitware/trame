from typing import Type, TypeVar, Generic

T = TypeVar("T")


class Singleton(Generic[T]):
    """Singleton decorator"""

    def __init__(self, cls: Type[T]):
        self._instance: T = cls()

    def __call__(self) -> T:
        return self._instance
