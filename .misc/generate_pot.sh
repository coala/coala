#!/bin/bash

set -x
set -e

cd ..
echo '' > locale/coala.pot
echo Generating new pot file...
cat `find . -name "*.py" \
 | grep -v build` coala \
  | python3 .misc/.extract_doc_translations > .doc_strings
xgettext -j -c --language=Python --output=locale/coala.pot --keyword=_ \
 --keyword=N_ --from-code=UTF-8 --package-name=coala \
 --package-version=`./coala --version` \
 --msgid-bugs-address=lasse.schuirmann@gmail.com \
 --copyright-holder="The coala authors" \
 `find . -name "*.py" | grep -v build` coala .doc_strings

echo Removing temporary files...
rm .doc_strings
echo Done.
echo
echo Please update the po files accordingly.
