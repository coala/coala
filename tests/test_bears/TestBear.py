from coalib.bears.LocalBear import LocalBear


class TestBear(LocalBear):

    def run(self, filename, file, result=False, exception: bool = False):
        if result is True:
            if file:
                for line in file:
                    yield line
            yield True
        elif result is not False:
            for item in result:
                yield item

        if exception:
            raise ValueError
