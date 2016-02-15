from bears.html.HTMLLintBear import HTMLLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear


test_file = """
<html>
  <body>
    <h1>Hello, world!</h1>
  </body>
</html>
""".split("\n")

HTMLLintBear1Test = verify_local_bear(HTMLLintBear,
                                      valid_files=(),
                                      invalid_files=(test_file,),
                                      tempfile_kwargs={"suffix": ".html"})

HTMLLintBear2Test = verify_local_bear(HTMLLintBear,
                                      valid_files=(test_file,),
                                      invalid_files=(),
                                      settings={
                                          'htmllint_ignore': 'optional_tag'},
                                      tempfile_kwargs={"suffix": ".html"})

HTMLLintBear3Test = verify_local_bear(HTMLLintBear,
                                      valid_files=(),
                                      invalid_files=(test_file,),
                                      settings={'htmllint_ignore': 'quotation'},
                                      tempfile_kwargs={"suffix": ".html"})
