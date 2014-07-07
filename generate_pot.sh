#!/bin/bash

mkdir -p tmp
echo '' > tmp/messages.po
echo Generating new pot file...
xgettext -j -c --language=Python --output=tmp/messages.po --keyword=_ --from-code=UTF-8 `find . -name "*.py" | grep -v build` codec
echo Merging with existent pot file...
msgmerge -N i18n/Codec.pot tmp/messages.po > i18n/Codec.pot 2> /dev/null
echo Removing temporary files...
rm -rf tmp
echo Done.
echo
echo Please update the po files accordingly.
