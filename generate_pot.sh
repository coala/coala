#!/bin/bash

mkdir -p tmp
echo '' > tmp/messages.po
echo Generating new pot file...
cat `find . -name "*.py" \
 | grep -v build` coala \
  | python3 .extract_doc_translations > tmp/doc_strings
xgettext -j -c --language=Python --output=tmp/messages.po --keyword=_ \
 --keyword=N_ --from-code=UTF-8 \
 `find . -name "*.py" | grep -v build` coala tmp/doc_strings


echo Merging with existent pot file...
msgmerge -N locale/coala.pot tmp/messages.po > locale/coala.pot 2> /dev/null
echo Removing temporary files...
rm -rf tmp
echo Done.
echo
echo Please update the po files accordingly.
