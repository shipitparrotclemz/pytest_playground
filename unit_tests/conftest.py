import pytest

from models.cup import Cup


@pytest.fixture(autouse=True)
def clear_class_attributes():
    Cup.clear_instances()