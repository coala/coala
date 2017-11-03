from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.LocalBear import LocalBear


class Test2LocalBear(LocalBear):
    LANGUAGES = {'C', 'Java'}


class Test2GlobalBear(GlobalBear):
    LANGUAGES = {'C'}
