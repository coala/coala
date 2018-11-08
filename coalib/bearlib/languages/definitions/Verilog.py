from coalib.bearlib.languages.Language import Language


@Language
class Verilog:
    aliases = 'verilog',
    extensions = '.v',
    comment_delimiters = '//',
    multiline_comment_delimiters = {'/*': '*/'}
    string_delimiters = {'"': '"'}
    encapsulators = {'(': ')', '[': ']', '{': '}'}
    string_delimiter_escape = {'"': '\\"', "'": "\\'"}
    line_continuation = '\\'
    keywords = [
        'always', 'and', 'assign', 'attribute', 'begin', 'buf', 'bufif0',
        'bufif1', 'case', 'casex', 'casez', 'cmos', 'deassign', 'default',
        'defparam', 'disable', 'edge', 'else', 'end', 'endattribute',
        'endcase', 'endfunction', 'endmodule', 'endprimitive', 'endspecify',
        'endtable', 'endtask', 'event', 'for', 'force', 'forever', 'fork',
        'function', 'highz0', 'highz1', 'if', 'ifnone', 'initial', 'inout',
        'input', 'integer', 'join', 'medium', 'module', 'large', 'macromodule',
        'nand', 'negedge', 'nmos', 'nor', 'not', 'notif0', 'notif1', 'or',
        'output', 'parameter', 'pmos', 'posedge', 'primitive', 'pull0',
        'pull1', 'pulldown', 'pullup', 'rcmos', 'real', 'realtime', 'reg',
        'release', 'repeat', 'rnmos', 'rpmos', 'rtran', 'rtranif0', 'rtranif1',
        'scalared', 'signed', 'small', 'specify', 'specparam', 'strength',
        'strong0', 'strong1', 'supply0', 'supply1', 'table', 'task', 'time',
        'tran', 'tranif0', 'tranif1', 'tri', 'tri0', 'tri1', 'triand', 'trior',
        'trireg', 'unsigned', 'vectored', 'wait', 'wand', 'weak0', 'weak1',
        'while', 'wire', 'wor', 'xnor', 'xor',
        ]
