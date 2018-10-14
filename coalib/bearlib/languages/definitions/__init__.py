"""
This directory holds language definitions.

Language definitions hold expressions that help defining specific syntax
elements for a programming language.

Currently defined keys are:

  names
  extensions
  comment_delimiters
  multiline_comment_delimiters
  string_delimiters
  multiline_string_delimiters
  keywords
  special_chars
  string_delimiter_escape
  max_line_length

When using quoting, if one wishes to represent the delimiter itself
in a string literal, one runs into the problem of `delimiter collision`.

For example, one cannot simply represent a statement like
`"This is "in quotes", but invalid."`.
In some languages, you can use `escape sequences` like
`"This is \"in quotes\" and properly escaped."` and in some others,
`doubling up` like `"This is ""in quotes"" and properly escaped."`
is used but there are many other solutions, depending mainly
on the language preference. All these result in the same thing
that is escaping of the quotation marks or the delimiters,
so these are collectively known as `string_delimiter_escape`.

More information regarding delimiter collision and
escaping delimiter solutions can be found here at
https://en.wikipedia.org/wiki/String_literal#Delimiter_collision.
"""
