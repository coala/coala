#!/bin/bash

cd ..
echo '' > locale/coala.pot
echo Generating new pot file...
cat `find . -name "*.py" \
 | grep -v build` coala \
  | python3 .misc/.extract_doc_translations > doc_strings
xgettext -j -c --language=Python --output=locale/coala.pot --keyword=_ \
 --keyword=N_ --from-code=UTF-8 \
 `find . -name "*.py" | grep -v build` coala doc_strings

echo Removing temporary files...
rm doc_strings
echo Done.
echo
echo Please update the po files accordingly.
