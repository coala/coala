from bears.tests.LocalBearTestHelper import verify_local_bear
from bears.natural_language.MarkdownBear import MarkdownBear


MarkdownBearTest = verify_local_bear(MarkdownBear,
                                     (["```\n", "some code\n", "```\n"],),
                                     (['    some code'],))
