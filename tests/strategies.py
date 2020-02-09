"""
Extending Hypothesis strategies for testing SeatingCharts
"""

import hypothesis.strategies as st


_not_str_or_int = st.one_of(
    st.binary(),
    st.booleans(),
    st.complex_numbers(),
    st.dates(),
    st.datetimes(),
    st.decimals(),
    st.floats(),
)

not_int = st.one_of(_not_str_or_int, st.characters(), st.text())

# Unused
nested_list = st.lists(st.lists(st.text()))
not_str = st.one_of(_not_str_or_int, st.integers())
non_str_list = st.lists(not_str)
