"""
seatingchart
~~~~~~~~~~~~

> What do you _mean_ we're not sitting together?
"""

import copy
import itertools
import random
from typing import Optional, List, Tuple, Union, Any

__version__ = "0.1.0"

# Type declarations
Roster = Optional[List[str]]
Pairs = Optional[List[Tuple[str, str]]]
Number = Optional[int]
Names = Union[str, List[str]]
Group = List[str]
Chart = List[Group]


class PositiveInteger(ValueError):
    """Raised when a value must be a positive integer."""


class GroupConflict(ValueError):
    """Raised when there's a collision in incompatible lists."""


class InvalidRequest(ValueError):
    """Raised when a valid seating chart cannot be made with the provided inputs."""


class SeatingChart:
    """
    Main class for seating chart logic.
    """

    def __init__(
        self,
        roster: Roster = None,
        together: Pairs = None,
        apart: Pairs = None,
        max_size: Number = None,
        num_groups: Number = None,
    ):
        """
        Args:
            roster (Roster): List of individuals included in the chart.
                Defaults to `None`.
            together (Pairs): List of pairs of individuals who should
                explicitly be grouped together. Defaults to `None`.
            apart (Pairs): List of pairs of individuals who should
                explicitly be separated. Defaults to `None`.
            max_size (Number): Maximum size of a single group. Defaults to
                unlimited (`None`).
            num_groups (Number): Maximum number of groups. Defaults to
                unlimited (`None`).
        """
        self.together, self.apart = self.__validate_together_apart(together, apart)
        self.max_size = self.__validate_integer_inputs(max_size)
        self.num_groups = self.__validate_integer_inputs(num_groups)

        # Roster validation must occur after we have validated `together` and
        # `apart`.
        self.roster = self.__validate_roster(roster)

        self.__chart = None

    # +--------------------+
    # | Data model methods |
    # +--------------------+

    def __repr__(self):
        return f"{self.__class__.__name__}: {len(self.roster)} Individuals, {len(self.chart)} Groups"

    def __len__(self):
        return len(self.chart)

    def __eq__(self, other):
        return self.chart == other.chart

    # +----------------+
    # | Public methods |
    # +----------------+

    @property
    def chart(self) -> Chart:
        """
        Returns generated seating chart, and creates it if it doesn't already
            exist.

        Returns:
            Chart: Seating chart.
        """
        if self.__chart is None:
            self.__chart = self.__generate_chart()
        return self.__chart

    def new(self) -> Chart:
        """
        Returns a new seating chart, even if one already exists.

        Returns:
            Chart: Seating chart.
        """
        self.__chart = self.__generate_chart()
        return self.__chart

    def add(
        self, name: Names = None, together: Pairs = None, apart: Pairs = None
    ) -> None:
        raise NotImplementedError

    def remove(
        self, name: Names = None, together: Pairs = None, apart: Pairs = None
    ) -> None:
        raise NotImplementedError

    def update(self, max_size: Number = False, num_groups: Number = False) -> None:
        """
        Updates the existing seating chart to meet an updated `max_size` or
        `num_groups` parameter.

        Args:
            max_size (Number): Maximum size of a single group.
            num_groups (Number): Maximum number of groups.
        """
        if max_size is not False:
            self.max_size = self.__validate_integer_inputs(max_size)

        if num_groups is not False:
            self.num_groups = self.__validate_integer_inputs(num_groups)

        self.__chart = self.__generate_chart()

        return

    # +-----------------+
    # | Private methods |
    # +-----------------+

    def __generate_chart(self) -> Chart:
        """
        Internal method that handles the many stages of actually creating and
        validating the chart at various stages of generation.

        Returns:
            Chart: Completed seating chart.
        """
        chart_1 = self.__handle_together()
        chart_2 = self.__handle_apart(chart_1)

        _ = self.__validate_group_size(chart_2)

        chart_3 = self.__handle_remaining(chart_2)

        _ = self.__validate_number_of_groups(chart_3)
        return chart_3

    def __handle_together(self) -> Chart:
        """
        Internal method that handles the grouping of explicit pairs
        (`together`).

        Returns:
            Chart: Seating chart with `together` pairs.
        """
        groups: list = []
        if self.together is None:
            return groups

        for pair in self.together:
            # Seed `groups` list if it's empty.
            if groups == []:
                groups.append(pair)
                continue

            pair_added_to_group = False
            for group in groups:
                group_pair_overlap = bool(set(pair) & set(group))

                # One or more members already exists in the group ->, add
                # remaining members to thar group.
                if group_pair_overlap:
                    group_pair_union = list(set(pair) | set(group))
                    groups.remove(group)
                    groups.append(group_pair_union)
                    pair_added_to_group = True
                    break

            if not pair_added_to_group:
                groups.append(pair)

        return sorted(groups, key=len, reverse=True)

    def __handle_apart(self, chart: Chart) -> Chart:
        """
        Internal method that handles the separation of explicit pairs
        (`apart`).

        Args:
            chart (Chart): Seating chart created by `__handle_together()`.

        Returns:
            Chart: Seating chart with `apart` pairs.
        """
        chart = copy.deepcopy(chart)

        if self.apart is None:
            return chart

        for pair in self.apart:
            item_1, item_2 = pair
            item_1_index = self.__get_nested_index(item_1, chart)
            item_2_index = self.__get_nested_index(item_2, chart)

            # 1. Chart is empty
            if chart == []:
                chart = [[item_1], [item_2]]

            # 2. Pair is already grouped, and members are in different lists; good!
            elif (
                item_1_index is not None
                and item_2_index is not None
                and item_1_index != item_2_index
            ):
                continue

            # 3. One pair member is grouped, other remaining.
            elif ((item_1_index is None) ^ (item_2_index is None)) and (
                (item_1_index is not None) ^ (item_2_index is not None)
            ):
                remaining_item = item_1 if item_1_index is None else item_2
                chart = self.__append_item(remaining_item, chart)

            # 4. Both remaining.
            elif item_1_index is None and item_2_index is None:
                chart = self.__append_item(item_1, chart)
                chart = self.__append_item(item_2, chart)

        return chart

    def __get_nested_index(self, item: str, chart: Chart) -> Number:
        """
        Returns the index of an item inside a nested list.

        Args:
            item (str): Variable we're searching for.
            chart (Chart): Seating chart.

        Returns:
            Number: Index of the list inside the nested list that contains
                `item`. Returns None if not found.
        """
        index = [chart.index(i) for i in chart if item in i]

        if len(index) == 0:
            return
        if len(index) == 1:
            return index[0]
        else:
            raise ValueError(f"Value '{item}' occurrs in more than one list.")

    def __append_item(self, item: str, chart: Chart) -> Chart:
        """
        Append an item to a chart, verifying that it obeys groups and
        separation rules.

        Args:
            item (str): Item being appended.
            chart (Chart): Nested list.

        Returns:
            Chart: Updated list with item appended.
        """
        chart = copy.deepcopy(chart)
        appended = False

        for index, group in enumerate(chart):
            if item in group:
                continue

            can_add_item_to_group = True
            for apart_pair in self.apart:
                if item not in apart_pair:
                    continue

                # Item we're appending has an "apart" constraint. Verify that
                # the group we're trying to add "item" to doesn't cause
                # conflict.
                apart_pair = copy.deepcopy(apart_pair)
                apart_pair.remove(item)
                conflict_item = apart_pair[0]

                if conflict_item in group:
                    can_add_item_to_group = False
                    break

            if can_add_item_to_group:
                if self.max_size is not None and len(group) >= self.max_size:
                    continue
                chart[index] += [item]
                appended = True

            if appended:
                break

        if not appended:
            chart.append([item])

        return chart

    def __handle_remaining(self, chart: Chart) -> Chart:
        """
        Internal method that handles individuals not specified in explicit
        pairings (e.g. `together` and `apart`).

        Args:
            chart (Chart): Seating chart created by `__handle_apart()`.

        Returns:
            Chart: Complete seating chart.
        """
        chart = copy.deepcopy(chart)
        already_placed = set(itertools.chain(*chart))
        remaining = set(copy.deepcopy(self.roster))

        remaining = list(remaining - already_placed)
        random.shuffle(remaining)

        for item in remaining:
            chart = self.__balance_nested_list(item, chart)

        return chart

    def __balance_nested_list(self, item: str, chart: Chart) -> Chart:
        """
        Helper method for adding a single item to a chart, in the matter that
        will best satisfy `max_size` and `num_groups` constraints.

        Args:
            item (str): Item being appended.
            chart (Chart): Nested list.

        Returns:
            Chart: Seating chart with `item` inserted.
        """
        chart = copy.deepcopy(chart)

        if chart == []:
            chart.append([item])
            return chart

        group_sizes = [len(i) for i in chart]
        all_same_len = len(set(group_sizes)) == 1
        max_group_size = max(group_sizes)
        num_current_groups = len(chart)
        index_min_size = group_sizes.index(min(group_sizes))

        if self.max_size is not None and self.max_size < max_group_size:
            raise InvalidRequest("Largest group exceeds `max_size` parameter")

        if (
            self.num_groups is not None
            and self.max_size is not None
            and self.num_groups < num_current_groups
            and self.max_size < max_group_size
        ):
            raise GroupConflict(
                "Number of groups is greater than value specified by `num_groups` "
                "and group size is greater than value specified by `max_size`."
            )

        if self.num_groups is not None and num_current_groups < self.num_groups:
            chart.append([item])
        elif (
            self.max_size is not None
            and all_same_len
            and (self.max_size <= max_group_size)
        ):
            chart.append([item])
        else:
            chart[index_min_size] += [item]

        return chart

    # +----------------+
    # | Helper methods |
    # +----------------+

    def __copy(self, item: Any) -> Any:
        """
        Returns a deepcopy of the item, or `None`.
        """
        if item is None:
            return
        return copy.deepcopy(item)

    # +--------------------+
    # | Validation methods |
    # +--------------------+

    def __validate_integer_inputs(self, number: Number) -> Number:
        """
        Ensures the input is a positive `int` or `None`, and returns the input.
        """
        if number is None:
            return
        if type(number) is not int:
            raise TypeError(f"{number} is a `{type(number)}`, and must be an `int`.")
        if number < 1:
            raise PositiveInteger(f"{number} must be greater than zero, or `None`.")
        return number

    def __validate_together_apart(
        self, together: Pairs, apart: Pairs
    ) -> Tuple[Pairs, Pairs]:
        """
        Ensures there are no collisions in `together` and `apart`.
        """
        together = self.__copy(together)
        apart = self.__copy(apart)

        if together is None or apart is None:
            return together, apart

        for pair_1, pair_2 in itertools.product(together, apart):
            if set(pair_1) == set(pair_2):
                raise GroupConflict(
                    f"Collision in `apart` and `together`: {pair_1} - {pair_2}."
                )

        return together, apart

    def __validate_roster(self, roster: Roster) -> Roster:
        """
        Ensures that the specified `roster` also includes all members in
        `together` and `apart`, and appends them if any are missing.
        """
        roster = self.__copy(roster)

        all_together_apart = set()
        if self.together is not None:
            for pair in self.together:
                all_together_apart |= set(pair)
        if self.apart is not None:
            for pair in self.apart:
                all_together_apart |= set(pair)

        # Nothing to verify because there were no pairs.
        if not all_together_apart:
            return roster

        # Add any individuals not in `roster` to the object.
        if roster is None:
            roster = []
        roster = set(roster)

        roster = list(roster | all_together_apart)
        return sorted(roster)

    def __validate_group_size(self, chart: Chart) -> None:
        """
        Ensures that no groups in the `chart` exceed the specified maximum
        group size (i.e. `max_size`).
        """
        if chart == []:
            return
        if self.max_size is not None and self.max_size < max([len(g) for g in chart]):
            raise ValueError(
                "One or more groups exceed the specified maximum group size."
            )
        return

    def __validate_number_of_groups(self, chart: Chart) -> None:
        """
        Ensures that the number of groups created doesn't exceed the specified
        number (i.e. `num_groups`).
        """
        if self.num_groups is not None and self.num_groups < len(chart):
            raise InvalidRequest(
                "Valid chart cannot be created. Please change the number of "
                "groups, max group size, or the together / apart groupings."
            )
        return

    # +----------------+
    # | Output Methods |
    # +----------------+

    def pretty(self) -> str:
        """
        Returns the seating chart as a pretty-printed string.
        """
        output = "Seating Chart:\n"
        for index, group in enumerate(self.chart):
            output += f"    Group {index + 1}: {self.__list_to_oxford_comma(group)}\n"
        return output

    def __list_to_oxford_comma(self, group: Group) -> str:
        """
        Helper method that returns a list as a comma-separated string.
        """
        if len(group) < 2:
            return " ".join(group)
        if len(group) == 2:
            return " and ".join(group)
        else:
            return ", ".join(group[:-1]) + ", and " + group[-1]
