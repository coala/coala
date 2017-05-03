from coalib.bears.LocalBear import LocalBear


class TestBear(LocalBear):

    def run(self, file, filename, result=False, exception: bool = False):
        if result is True:
            yield True
        elif result is not False:
            for item in result:
                yield item

        if exception:
            raise ValueError
