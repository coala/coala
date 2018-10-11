from coalib.bearlib.languages.Language import Language


@Language
class CSS:
    extensions = '.css',
    multiline_comment_delimiters = {'/*': '*/'}
    string_delimiters = {'"': '"', "'": "'"}
    multiline_string_delimiters = {}
    indent_types = {'{': '}'}
    encapsulators = {'(': ')', '[': ']'}
    string_delimiter_escape = {'"': '\\"', "'": "\\'"}
@Language 
class SASS: 
     
class {
	CSS {
		&: {
			extensions {
				= {
					'.css' {
						'/*': '*/';
					}
				}
			}
		}
	}
}
multiline_comment_delimiters {
	= {
		'/*': '*/';
	}
}
string_delimiters {
	= {
		'"': '"', "'": "'";
	}
}
indent_types {
	= {
		'{': '}';
	}
}
encapsulators {
	= {
		'(': ')', '[': ']';
	}
}
string_delimiter_escape {
	= {
		'"': '\\"', "'": "\\'";
	}
}

