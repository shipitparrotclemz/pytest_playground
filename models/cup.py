from enum import Enum


class CupSize(str, Enum):
    small = "Small"
    medium = "Medium"
    large = "Large"


class Cup:
    """
    In a unit test,
    we want to ensure all unit unit_tests do not share state

    class attributes are usually overlooked as shared state across unit unit_tests

    In this experiment, we will attempt clearing the global attribute of the class
    for all unit unit_tests
    """

    _instances: set["Cup"] = set()

    def __init__(self, name: str | None = None, size: CupSize | None = None) -> None:
        self._name = name
        self._size = size
        self._instances.add(self)

    @property
    def name(self) -> str | None:
        return self._name

    @property
    def size(self) -> CupSize | None:
        return self._size

    @classmethod
    def clear_instances(cls) -> None:
        """
        Clears the `_instances` class attribute
        """
        cls._instances.clear()
