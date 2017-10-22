from coalib.bears.LocalBear import LocalBear


class TestDepBearA(LocalBear):

    def run(self, filename, file, settings1='', settings2=''):
        yield [settings1, settings2]


class TestDepBearAA(LocalBear):

    def run(self, filename, file, settings3='', settings4=''):
        yield [settings3, settings4]


class TestDepBearDependsAAndAA(LocalBear):

    BEAR_DEPS = {TestDepBearA, TestDepBearAA}

    def run(self, filename, file, dependency_results):
        dep_resultA = dependency_results[TestDepBearA.name][0]
        dep_resultAA = dependency_results[TestDepBearAA.name][0]
        yield dep_resultA + dep_resultAA


class TestDepBearBDependsA(LocalBear):

    BEAR_DEPS = {TestDepBearA}

    def run(self, filename, file, dependency_results,
            settings3='', settings4=''):
        dep_result = dependency_results[TestDepBearA.name][0]
        yield dep_result + [settings3, settings4]


class TestDepBearCDependsB(LocalBear):

    BEAR_DEPS = {TestDepBearBDependsA}

    def run(self, filename, file, dependency_results,
            settings5='', settings6=''):
        dep_result = dependency_results[TestDepBearBDependsA.name][0]
        yield dep_result + [settings5, settings6]
