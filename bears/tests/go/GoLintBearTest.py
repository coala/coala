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
// Test that blank imports in library packages are flagged.

// Package foo ...
package foo

// The instructions need to go before the imports below so they will not be
// mistaken for documentation.

/* MATCH /blank import/ */ import _ "encoding/json"

import (
  "fmt"

  /* MATCH /blank import/ */ _ "os"

  /* MATCH /blank import/ */ _ "net/http"
  _ "path"
)

import _ "encoding/base64" // Don't gripe about this

import (
  // Don't gripe about these next two lines.
  _ "compress/zlib"
  _ "syscall"

  /* MATCH /blank import/ */ _ "path/filepath"
)

import (
  "go/ast"
  _ "go/scanner" // Don't gripe about this or the following line.
  _ "go/token"
)

var (
  _ fmt.Stringer // for "fmt"
  _ ast.Node     // for "go/ast"
)
""".split("\n")


GoLintBearTest = verify_local_bear(GoLintBear,
                                   valid_files=(good_file,),
                                   invalid_files=(bad_file,))


GoLintBearTest = verify_local_bear(
    GoLintBear,
    valid_files=(),
    invalid_files=(bad_file,),
    settings={"golint_cli_options": "-min_confidence=0.8"})
