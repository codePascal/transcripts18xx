#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""State Verification Runner

Module implements a state verification that compares the parsed player and
company states to a ground truth.
"""


class StateVerification(object):
    """StateVerification

    Class implements the functionality to compare two dictionaries and highlight
    differences.

    Attributes:
        _missing: Key to indicate that value or key is missing in either dict.
    """

    def __init__(self):
        self._missing = '<missing>'

    def run(self, parsed: dict, ground_truth: dict) -> bool:
        """Runs the comparison of the two state dicts.

        Args:
            parsed: The parsed state of the pipeline.
            ground_truth: The ground truth.

        Returns:
            True if the two dicts are identical, False otherwise.
        """
        diffs = self._compare_nested_dicts(parsed, ground_truth)
        self._display_differences(diffs)
        success = self._evaluate_differences(diffs)
        return success

    @staticmethod
    def _display_differences(diffs: dict) -> None:
        # Print differences of the two dicts.
        print('===================================')
        print('State Differences: Parsed vs. Truth')
        print('-----------------------------------')
        for path, (v1, v2) in diffs.items():
            print(f'{path}: {v1!r} != {v2!r}')
        print('-----------------------------------')

    def _evaluate_differences(self, diffs: dict) -> bool:
        # If left side is `<missing>`, that is fine.
        left_side = set([v1 for (v1, v2) in diffs.values()])
        if len(left_side) == 1 and list(left_side)[0] == self._missing:
            return True
        return False

    def _compare_nested_dicts(self, d1, d2, path: str = str()) -> dict:
        # Compare dictionaries recursively.
        diffs = {}
        all_keys = set(d1.keys()) | set(d2.keys())
        for key in all_keys:
            full_path = f'{path}.{key}' if path else key
            if key not in d1:
                diffs[full_path] = (self._missing, d2[key])
            elif key not in d2:
                diffs[full_path] = (d1[key], self._missing)
            else:
                val1, val2 = d1[key], d2[key]
                if isinstance(val1, dict) and isinstance(val2, dict):
                    sub_diffs = self._compare_nested_dicts(
                        val1, val2, full_path
                    )
                    diffs.update(sub_diffs)
                elif val1 != val2:
                    diffs[full_path] = (val1, val2)
        return diffs
