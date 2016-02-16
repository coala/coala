from bears.js.JSONFormatBear import JSONFormatBear
from bears.tests.LocalBearTestHelper import verify_local_bear

test_file1 = """{
    "a": 5,
    "b": 5
}""".split("\n")


test_file2 = """{
    "b": 5,
    "a": 5
}""".split("\n")

test_file3 = """{
   "b": 5,
   "a": 5
}""".split("\n")


JSONFormatBear1Test = verify_local_bear(JSONFormatBear,
                                        valid_files=(test_file1, test_file2),
                                        invalid_files=(test_file3,
                                                       [""],
                                                       ["random stuff"],
                                                       ['{"a":5,"b":5}']))


JSONFormatBear2Test = verify_local_bear(JSONFormatBear,
                                        valid_files=(test_file1,),
                                        invalid_files=(test_file2,),
                                        settings={"json_sort": "true"})


JSONFormatBear3Test = verify_local_bear(JSONFormatBear,
                                        valid_files=(test_file3,),
                                        invalid_files=(test_file2),
                                        settings={"tab_width": "3"})
