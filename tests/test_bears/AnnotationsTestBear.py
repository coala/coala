from coalib.bearlib.type_annotations.Annotations import (
    add_value_checks)
from coalib.bears.LocalBear import LocalBear


class AnnotationsTestBear(LocalBear):
    @add_value_checks(
        [('number', [3, 4]),
         ('fruit', ['mango', 'banana']),
         ('d', [5, 6, 'pineapple'])])
    def run(self, number, fruit, c=True, d=5):
        pass
