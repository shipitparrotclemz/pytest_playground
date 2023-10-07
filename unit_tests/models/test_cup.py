from models.cup import Cup, CupSize


class TestCup:
    def test_cup_name(self) -> None:
        assert len(Cup._instances) == 0
        cup: Cup = Cup(name="Donald")
        assert cup.name == "Donald"

    def test_cup_size(self) -> None:
        assert len(Cup._instances) == 0
        cup: Cup = Cup(size=CupSize.small)
        assert cup.size == CupSize.small
