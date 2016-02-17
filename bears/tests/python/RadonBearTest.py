from bears.python.RadonBear import RadonBear
from bears.tests.LocalBearTestHelper import verify_local_bear

test_file1 = """
def simple():
    pass
""".splitlines()


test_file2 = """
class class1():
    pass
""".splitlines()


RadonBear1Test = verify_local_bear(RadonBear,
                                   valid_files=(test_file1, test_file2),
                                   invalid_files=(),
                                   settings={
                                       "radon_ranks_info": "",
                                       "radon_ranks_normal": "",
                                       "radon_ranks_major": ""})


RadonBear2Test = verify_local_bear(RadonBear,
                                   valid_files=(),
                                   invalid_files=(test_file1, test_file2),
                                   settings={
                                       "radon_ranks_info": "",
                                       "radon_ranks_normal": "A",
                                       "radon_ranks_major": ""})
