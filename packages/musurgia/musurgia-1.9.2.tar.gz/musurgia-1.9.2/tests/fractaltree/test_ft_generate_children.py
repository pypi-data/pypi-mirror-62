from unittest import TestCase

from musurgia.fractaltree.fractaltree import FractalTree


class Test(TestCase):
    def setUp(self) -> None:
        self.ft = FractalTree(value=10)

    def test_1(self):
        self.ft.generate_children(number_of_children=0)
        result = [None]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_2(self):
        ft = self.ft
        ft.generate_children(number_of_children=1)
        result = [3]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_3(self):
        ft = self.ft
        ft.generate_children(number_of_children=2)
        result = [3, 2]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_4(self):
        ft = self.ft
        ft.generate_children(number_of_children=3)
        result = [3, 1, 2]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_5(self):
        ft = self.ft
        with self.assertRaises(ValueError):
            ft.generate_children(number_of_children=4)

    def test_6(self):
        ft = self.ft
        ft.generate_children(number_of_children=(1, 1, 1))
        result = [[3], [3], [3]]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_7(self):
        ft = self.ft
        ft.generate_children(number_of_children=(0, 1, 2))
        result = [[2, 3], 1, [3]]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_8(self):
        ft = self.ft
        ft.generate_children(number_of_children=(1, 2, (1, 2, 3)))
        result = [
            [[3], [2, 3], [3, 1, 2]],
            [3],
            [2, 3]
        ]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_9(self):
        ft = self.ft
        ft.generate_children(
            number_of_children=(
                (1, 3),
                2,
                (1,
                 (1, 3),
                 3)
            )
        )
        result = [
            [
                [3],
                [
                    [3],
                    [2, 3, 1]
                ],
                [3, 1, 2]
            ],
            [
                [3, 1, 2],
                [3]
            ],
            [2, 3]
        ]
        self.assertEqual(result, self.ft.get_leaves(key=lambda leaf: leaf.fractal_order))

    def test_10(self):
        ft = FractalTree(value=10, proportions=(1, 2, 3, 4, 5, 6, 7), tree_permutation_order=(2, 6, 4, 1, 3, 7, 5))
        ft.generate_children(mode='merge', number_of_children=2)
        test_case = ft.get_leaves(key=lambda leaf: float(leaf.value))
        expected = [8.214285714285714, 1.7857142857142858]
        self.assertEqual(expected, test_case)
