from bears.go.GoLintBear import GoLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear

good_file = """
// Test that blank imports in package main are not flagged.
// OK

// Binary foo ...
package main

import _ "fmt"

import (
  "os"
  _ "path"
)

var _ os.File // for "os"
""".split("\n")


bad_file = """
package pkg

func addOne(x int) int {
  x += 1
  return x
}

func subOneInLoop(y int) {
  for ; y > 0; y -= 1 {
  }
}
""".split("\n")


GoLintBear1Test = verify_local_bear(GoLintBear,
                                    valid_files=(good_file,),
                                    invalid_files=(bad_file,))


GoLintBear2Test = verify_local_bear(
    GoLintBear,
    valid_files=(bad_file, good_file),
    invalid_files=(),
    settings={"golint_cli_options": "-min_confidence=1"})
