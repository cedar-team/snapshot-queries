import unittest

from snapshot_queries.testing.assert_queries_match_mixin import _diff_lists_detailed


class DiffListsTestCase(unittest.TestCase):
    def test_empty_lists(self):
        self.assertEqual(_diff_lists_detailed([], []), ([], []))

    def test_item_added(self):
        self.assertEqual(_diff_lists_detailed([], ["added"]), ([(0, "added")], []))

    def test_item_removed(self):
        self.assertEqual(_diff_lists_detailed(["removed"], []), ([], [(0, "removed")]))

    def test_item_changed(self):
        self.assertEqual(_diff_lists_detailed(["1"], ["2"]), ([(0, "2")], [(0, "1")]))

    def test_swap(self):
        self.assertEqual(
            _diff_lists_detailed(["1", "2"], ["2", "1"]), ([(1, "1")], [(0, "1")])
        )

    def test_move(self):
        self.assertEqual(
            _diff_lists_detailed(["1", "2", "3", "4"], ["1", "3", "4", "2"]),
            ([(3, "2")], [(1, "2")]),
        )

    def test_item_added_end(self):
        self.assertEqual(_diff_lists_detailed(["1"], ["1", "2"]), ([(1, "2")], []))

    def test_item_added_beginning(self):
        self.assertEqual(_diff_lists_detailed(["2"], ["1", "2"]), ([(0, "1")], []))

    def test_item_added_middle(self):
        self.assertEqual(
            _diff_lists_detailed(["1", "3"], ["1", "2", "3"]), ([(1, "2")], [])
        )

    def test_item_removed_beginning(self):
        self.assertEqual(_diff_lists_detailed(["1", "2"], ["2"]), ([], [(0, "1")]))

    def test_item_removed_end(self):
        self.assertEqual(_diff_lists_detailed(["1", "2"], ["1"]), ([], [(1, "2")]))

    def test_item_removed_middle(self):
        self.assertEqual(
            _diff_lists_detailed(["1", "2", "3"], ["1", "3"]), ([], [(1, "2")])
        )

    def test_complex_remove(self):
        self.assertEqual(
            _diff_lists_detailed(
                ["1", "2", "3", "4", "5", "6", "7"], ["1", "2", "4", "7"]
            ),
            ([], [(2, "3"), (4, "5"), (5, "6")]),
        )

    def test_complex_add(self):
        self.assertEqual(
            _diff_lists_detailed(["2", "3", "6"], ["1", "2", "3", "4", "5", "6", "7"]),
            ([(0, "1"), (3, "4"), (4, "5"), (6, "7")], []),
        )

    def test_complex_add_and_remove(self):
        self.assertEqual(
            _diff_lists_detailed(
                ["1", "2", "3", "4", "5", "6", "7"],
                ["8", "3", "9", "5", "6", "7", "10"],
            ),
            ([(0, "8"), (2, "9"), (6, "10")], [(0, "1"), (1, "2"), (3, "4")]),
        )
