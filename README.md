# Pytest Playground - Global pytest fixtures

## Context

Unit tests have 5 important properties

1. They must not share state between them
2. They should only use fixtures with scope="function" (default), and not "module" and "session"
3. They must not call external services
4. The order of running them does not matter
5. They can be parallelized

However, multiple class attributes defined in a large repository are often over-looked "shared state" across the unit tests.

We can use a pytest fixture to clear these class attributes prior to running each unit test

However it is very tedious to manually mark all unit tests to use the fixture.

In this repository, we experiment with placing a global pytest fixture in `conftest.py`, and test that all unit tests automatically runs it.

## Setup

### Activate the poetry environment

```commandline
poetry shell
```

### Install dependencies

```commandline
poetry shell
```

## Defining a class with a Class Attribute

The class is defined in `models/cup.py`

It contains a single class `Cup`, with a class attribute `_instances`

We modified the constructor to add the instance into this class attribute.

Each creation of a Cup object will add the instance into it.

## Defining the two unit tests, which share the same state `Cup._instances`

Now, we create two unit tests in `unit_tests/models/test_cup.py`

In each of these unit tests, we create an instance of `Cup`

By default, without any pytest fixture to clear the class `_instances` attribute, the two unit tests will technically share the same state of `Cup._instances`

To make this clearer, we place an assert statement at start of each unit test, to check that the state is indeed cleared prior to running it.

```commandline
class TestCup:
    def test_cup_name(self) -> None:
        assert len(Cup._instances) == 0
        cup: Cup = Cup(name="Donald")
        assert cup.name == "Donald"

    def test_cup_size(self) -> None:
        assert len(Cup._instances) == 0
        cup: Cup = Cup(size=CupSize.small)
        assert cup.size == CupSize.small
```

## Running the pytest - Without clearing the `Cup._attributes` prior to running the unit tests

```commandline
pytest unit_tests.py
```

We will see that the second test fails, since at the start of the second test `TestCup.test_cup_size`, the `Cup._instances` already has a single instance of Cup in it.

This instance of Cup was created by the first test `TestCup.test_cup_name` prior to it.

```commandline
____________________________________________________________________________ TestCup.test_cup_size _____________________________________________________________________________

self = <test_cup.TestCup object at 0x101a41250>

    def test_cup_size(self) -> None:
>       assert len(Cup._instances) == 0
E       assert 1 == 0
E        +  where 1 = len({<models.cup.Cup object at 0x101a07b50>})
E        +    where {<models.cup.Cup object at 0x101a07b50>} = Cup._instances

unit_tests/models/test_cup.py:11: AssertionError
=========================================================================== short test summary info ============================================================================
FAILED unit_tests/models/test_cup.py::TestCup::test_cup_size - assert 1 == 0
========================================================================= 1 failed, 1 passed in 0.02s ==========================================================================
```

## Fixing the shared state, by defining a global pytest fixture which will run before each test

We define a `conftest.py` file in the unit test directory (`unit_tests`)

In there, we specify a pytest fixture, a function, decorated with the `pytest.fixture` function decorator.

This pytest fixture is responsible for preparing the conditions for the unit test, prior to running it.

By providing the pytest fixture function decorator with `autouse=True`, and specifying it in the special file `conftest.py`, it will be executed before any unit test in the directory.

```conftest.py
import pytest

from models.cup import Cup


@pytest.fixture(autouse=True)
def clear_class_attributes():
    Cup.clear_instances()
```

## Running the unit tests with the new pytest.fixture

Our unit tests indeed passes, proving that the unit tests indeed have the `Cup._instances` attribute reset to an empty set prior to running each unit test.

```commandline
=========================================================================== short test summary info ============================================================================
FAILED unit_tests/models/test_cup.py::TestCup::test_cup_size - assert 1 == 0
========================================================================= 1 failed, 1 passed in 0.02s ==========================================================================
(pytest-playground-py3.11) clement@Clements-Laptop pytest_playground % pytest unit_tests
============================================================================= test session starts ==============================================================================
platform darwin -- Python 3.11.5, pytest-7.4.2, pluggy-1.3.0
rootdir: /Users/clement/Desktop/ship_it_parrot/pytest_playground
collected 2 items                                                                                                                                                              

unit_tests/models/test_cup.py ..                                                                                                                                         [100%]

============================================================================== 2 passed in 0.00s ===============================================================================
```