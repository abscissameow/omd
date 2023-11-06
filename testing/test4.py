import pytest
from typing import List, Tuple


def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows


class TestFitTransform:

    def test_single_word(self):
        assert fit_transform('мяу') == [('мяу', [1])]

    def test_different_words(self):
        assert fit_transform('мяу', 'мур', 'хрю') == [('мяу', [0, 0, 1]),
                                                      ('мур', [0, 1, 0]),
                                                      ('хрю', [1, 0, 0])]

    def test_same_words(self):
        assert fit_transform('мяу', 'мяу', 'мяу') == [('мяу', [1]),
                                                      ('мяу', [1]),
                                                      ('мяу', [1])]

    def test_mixed_words(self):
        assert fit_transform('мяу', 'мур', 'мяу', 'хрю', 'хрю') == [('мяу', [0, 0, 1]),
                                                                    ('мур', [0, 1, 0]),
                                                                    ('мяу', [0, 0, 1]),
                                                                    ('хрю', [1, 0, 0]),
                                                                    ('хрю', [1, 0, 0])]

    def test_exception(self):
        with pytest.raises(TypeError):
            fit_transform(123)


if __name__ == "__main__":
    pytest.main()
