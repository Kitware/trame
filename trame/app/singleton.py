from typing import Type, TypeVar, Generic

T = TypeVar("T")


class Singleton(Generic[T]):
    """
    Class decorator to make it a Singleton

    This is useful when you want a central engine instance or else
    to be used across your application modules.

    But using such decorator will make it tricky or impossible to
    use your application within several server using the same
    event loop.
    """

    def __init__(self, cls: Type[T]):
        self._instance: T = cls()

    def __call__(self) -> T:
        return self._instance


__all__ = [
    "Singleton",
]
