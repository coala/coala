from __future__ import print_function

import os.path
import sys

from collections import defaultdict

from pygments.lexers import (
    get_all_lexers,
    get_lexer_by_name,
)
from pygments.token import (
    Comment,
)
from coalib.bearlib.languages.Language import (
    LanguageUberMeta,
)


coalang_dir = 'coalib/bearlib/languages/definitions'
coalangs = LanguageUberMeta.all
known_extensions = defaultdict(list)


def fill_known_extensions():
    expected = len(coalangs)
    count = 0

    for lang in coalangs:
        count += 1

        assert count <= expected, '%d > %d' % (count, expected)

        ilang = lang()

        versioned_langs = []

        for version in ilang.versions:
            versioned_langs.append(lang(version))

        if not versioned_langs:
            versioned_langs = [ilang]

        for versioned_lang in versioned_langs:
            try:
                exts = versioned_lang.extensions
            except (KeyError, AttributeError):
                print('Skipping %s: no extensions' % versioned_lang,
                      file=sys.stderr)
                continue

            for ext in exts:
                print('%r' % ext)
                known_extensions[ext].append(lang)


def get_extensions(lexer):
    exts = [ext.lstrip('*') for ext in lexer.filenames
            if '[' not in ext
            and not ext.endswith('*')]
    for ext in [ext for ext in lexer.filenames if ext.endswith(']')]:
        print('Expanding %s' % ext)
        ext = ext.lstrip('*')
        start = ext.find('[')
        for char in ext[start+1:-1]:
            exts.append('%s%s' % (ext[:start], char))

    return exts


def get_attributes(lexer):
    attrs = {
        'comment_delimiter': None,
    }
    for section, entries in lexer.tokens.items():
        for entry in entries:
            if not isinstance(entry, tuple):
                continue
            if entry[1] == Comment.Single:
                if entry[0] == r'//.*?\n':
                    attrs['comment_delimiter'] = '//'

    return attrs


def write_lexer(lexer):
    if not hasattr(lexer, 'tokens'):
        print('Skipping %s: no tokens' % lexer.name, file=sys.stderr)
        return

    name = lexer.name
    name = name.replace(' ', '')
    name = name.replace('+', '_')
    name = name.replace('/', '')
    name = name.replace('-', '')
    name = name.replace('.', '')

    filename = '%s/%s.py' % (coalang_dir, name)

    if not lexer.filenames:
        print('Skipping %s: no filenames' % lexer.name, file=sys.stderr)
        return

    exts = ["'%s'" % ext for ext in get_extensions(lexer)]
    exts = ', '.join(exts) if len(exts) > 1 else '%s,' % exts[0]

    attrs = get_attributes(lexer)
    if attrs:
        print(attrs)

    with open(filename, 'w') as f:
        f.write('from coalib.bearlib.languages.Language import Language\n')
        f.write('\n')
        f.write('\n')
        f.write('@Language\n')
        f.write('class %s:\n' % name)
        f.write("    extensions = %s\n" % exts)

    print('Wrote %s' % filename, file=sys.stderr)


def write_init():
    filenames = list(os.listdir(coalang_dir))
    with open('coalib/bearlib/languages/__init__.py', 'w') as f:
        f.write("""\"\"\"
This directory holds means to get generic information for specific languages.
\"\"\"

from .Language import Language
from .Language import Languages

""")

        for filename in sorted(filenames):
            if filename.startswith('__'):
                continue
            name = os.path.splitext(filename)[0]
            f.write('from .definitions.%s import %s\n' % (name, name))


def process_pygments():
    gen = get_all_lexers()
    for lexer in gen:
        lexer = get_lexer_by_name(lexer[1][0])
        name = lexer.name
        exts = get_extensions(lexer)
        found = False
        for ext in exts:
            if found:
                continue
            if ext in known_extensions:
                if (isinstance(known_extensions[ext], bool)
                        and known_extensions[ext] is True):
                    print('Pygments lexer %s is likely to be already added'
                          % (name),
                          file=sys.stderr)
                elif len(known_extensions[ext]) > 1:
                    print('Pygments lexer %s maps to multiple coalang %r'
                          % (name, known_extensions[ext]),
                          file=sys.stderr)
                else:
                    print('Pygments lexer %s is likely to be coalang %s'
                          % (name, known_extensions[ext][0].__qualname__),
                          file=sys.stderr)
                found = True
                continue

        if found:
            continue

        write_lexer(lexer)
        for ext in exts:
            known_extensions[ext] = True


print('Known languages: ', coalangs)
fill_known_extensions()
print('Known extensions: %s' % ', '.join(sorted(known_extensions.keys())))
process_pygments()
write_init()
