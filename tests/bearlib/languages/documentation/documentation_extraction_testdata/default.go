/*
Comments may span
multiple lines
*/
package main

import (
    "fmt"
)

// A class comment
// that also spans
// multiple lines
type Result struct {
    code int
}

// More documentation for everyone, but in one line
func main() {
    fmt.Println(Result{code: 200})
}
