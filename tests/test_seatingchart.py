from hypothesis import given
import hypothesis.strategies as st
import pytest

from seatingchart import __version__
from seatingchart import SeatingChart
from seatingchart import PositiveInteger, GroupConflict

from tests.strategies import not_int


@pytest.fixture()
def roster():
    return ["Amy", "Bob", "Cara", "Dan", "Emma", "Felix", "Gail", "Hank"]


@pytest.fixture()
def together():
    return [["Amy", "Bob"], ["Gail", "Hank"]]


@pytest.fixture()
def apart():
    return [["Amy", "Dan"], ["Dan", "Felix"]]


def test_version():
    assert __version__ == "0.1.0"


class TestValidateIntegerInputs:
    """
    SeatingChart's `max_size` and `num_groups` arguments rely on the
    `__validate_integer_inputs()` method.
    """

    @given(data=st.integers(min_value=1))
    def test_max_size_positive_integers(self, data):
        _ = SeatingChart(max_size=data)

    @given(data=st.none())
    def test_max_size_none(self, data):
        _ = SeatingChart(max_size=data)

    @given(data=st.integers(max_value=0))
    def test_max_size_non_positive_integers(self, data):
        with pytest.raises(PositiveInteger):
            _ = SeatingChart(max_size=data)

    @given(data=not_int)
    def test_max_size_not_integer(self, data):
        with pytest.raises(TypeError):
            _ = SeatingChart(max_size=data)

    @given(data=st.integers(min_value=1))
    def test_num_groups_positive_integers(self, data):
        _ = SeatingChart(num_groups=data)

    @given(data=st.none())
    def test_num_groups_none(self, data):
        _ = SeatingChart(num_groups=data)

    @given(data=st.integers(max_value=0))
    def test_num_groups_non_positive_integers(self, data):
        with pytest.raises(PositiveInteger):
            _ = SeatingChart(num_groups=data)

    @given(data=not_int)
    def test_num_groups_not_integer(self, data):
        with pytest.raises(TypeError):
            _ = SeatingChart(num_groups=data)


class TestValidateTogetherApart:
    """
    SeatingChart's `together` and `apart` arguments rely on the
    `__validate_together_apart()` method.
    """

    def test_together_only(self):
        _ = SeatingChart(together=[["A", "B"], ["C", "D"]])

    def test_apart_only(self):
        _ = SeatingChart(apart=[["A", "B"], ["C", "D"]])

    def test_apart_together_intersect(self):
        with pytest.raises(GroupConflict):
            _ = SeatingChart(together=[["A", "B"]], apart=[["A", "B"]])

    def test_apart_together_disjoint(self):
        _ = SeatingChart(together=[["A", "B"]], apart=[["C", "D"]])


class TestChart:
    """
    Test SeatingChart public methods.
    """

    def test_num_groups(self, roster):
        sc = SeatingChart(roster=roster, num_groups=2)
        assert len(sc.chart) == 2

    def test_max_size(self, roster):
        sc = SeatingChart(roster=roster, max_size=1)
        assert len(sc.chart) == len(roster)

    def test_new(self, roster):
        sc = SeatingChart(roster=roster, num_groups=4)
        original_chart = sc.chart
        new_chart = sc.new()
        assert original_chart != new_chart

    def test_update_max_size(self, roster):
        sc = SeatingChart(roster=roster, max_size=4)
        original_chart = sc.chart
        _ = sc.update(max_size=2)
        updated_chart = sc.chart
        assert original_chart != updated_chart

        for subgroup in updated_chart:
            assert len(subgroup) <= 2

    def test_update_num_groups(self, roster):
        sc = SeatingChart(roster=roster, num_groups=4)
        original_chart = sc.chart
        _ = sc.update(num_groups=2)
        updated_chart = sc.chart

        assert original_chart != updated_chart
        assert len(updated_chart) == 2

    def test_together_only(self, roster, together):
        sc = SeatingChart(roster=roster, together=together)

        for person_1, person_2 in together:
            for group in sc.chart:
                if person_1 in group:
                    assert person_2 in group

    def test_apart_only(self, roster, apart):
        sc = SeatingChart(roster=roster, apart=apart)

        for person_1, person_2 in apart:
            for group in sc.chart:
                if person_1 in group:
                    assert person_2 not in group

    def test_together_and_apart(self, roster, together, apart):
        sc = SeatingChart(roster=roster, together=together, apart=apart)

        for person_1, person_2 in together:
            for group in sc.chart:
                if person_1 in group:
                    assert person_2 in group

        for person_1, person_2 in apart:
            for group in sc.chart:
                if person_1 in group:
                    assert person_2 not in group


class TestInternalMethods:
    """
    Test internal, helper methods in the SeatingChart class.
    """

    def test_balance_nested_list(self):
        sc = SeatingChart()
        value = "1"

        nested_1 = [["0", "0", "0", "0"], ["0", "0", "0"], ["0", "0"]]
        nested_1 = sc._SeatingChart__balance_nested_list(value, nested_1)
        assert nested_1 == [["0", "0", "0", "0"], ["0", "0", "0"], ["0", "0", "1"]]

        nested_2 = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
        sc.max_size = 3
        nested_2 = sc._SeatingChart__balance_nested_list(value, nested_2)
        assert nested_2 == [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"], ["1"]]

        nested_3 = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
        sc.max_size = None
        sc.num_groups = 3
        nested_3 = sc._SeatingChart__balance_nested_list(value, nested_3)
        assert nested_3 == [["0", "0", "0", "1"], ["0", "0", "0"], ["0", "0", "0"]]
