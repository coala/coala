import os

from bears.js.ESLintBear import ESLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear
from coalib.misc.ContextManagers import prepare_file


test_good = """
function addOne(i) {
    if (!isNaN(i)) {
        return i+1;
    }
    return i;
}

addOne(3);

""".split('\n')

test_bad = """
function addOne(i) {
    if (i != NaN) {
        return i ++
    }
    else {
        return
    }
};
""".split('\n')

config = """
{
    "rules": {
        "indent": [1, 4]
    }
}
""".split('\n')

eslintconfig = os.path.join(os.path.dirname(__file__),
                            "test_files",
                            ".eslintrc")

ESLintBearGoodTest = verify_local_bear(ESLintBear,
                                       valid_files=(test_good,),
                                       invalid_files=(),
                                       settings={"eslint_config":
                                                 eslintconfig})

ESLintBearBadTest = verify_local_bear(ESLintBear,
                                      valid_files=(),
                                      invalid_files=(test_bad,),
                                      settings={"eslint_config":
                                                eslintconfig})

with prepare_file(config,
                  filename=None,
                  force_linebreaks=True,
                  create_tempfile=True) as (conf_lines, conf_file):
    ESLintBearConfigTest = verify_local_bear(ESLintBear,
                                             valid_files=(test_bad, test_good),
                                             invalid_files=(),
                                             settings={"eslint_config":
                                                       conf_file})
