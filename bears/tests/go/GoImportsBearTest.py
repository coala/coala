
from bears.tests.LocalBearTestHelper import verify_local_bear
from bears.go.GoImportsBear import GoImportsBear

GoImportsBearTest = verify_local_bear(
    GoImportsBear,
    (['package main', '', 'import "os"', '',
      'func main() {', '\tf, _ := os.Open("foo")', '}'],),
    (['package main', '', '',
      'func main() {', '\tf, _ := os.Open("foo")', '}'],))
