set -x
set -e

source install.zanata.sh

echo Pulling translations...
$zanata -B pull --url https://translate.zanata.org/zanata/ > /dev/null

echo Committing translation update...
git add ../locale/*.po
git commit -m "[GENERATED] Update Translations from zanata"

echo Done.
