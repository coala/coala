set -x
set -e

# Disable things that circleci starts that we do not need
sudo service mysql stop
sudo service mongodb stop
sed -i '/source \/home\/ubuntu\/virtualenvs\//d' ~/.circlerc

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 0) dep_versions=( "3.2.6" "3.3.6" "3.4.2" ) ;;
 1) dep_versions=( "3.3.6" ) ;;
 2) dep_versions=( "3.2.6" ) ;;
 *) dep_versions=( "3.4.2" ) ;;
esac

# Install python version needed
# Note - `--with-wide-unicode` is needed only because 3.2.5 defaults to UCS2 unicode

for dep_version in "${dep_versions[@]}" ; do
  PYTHON_CONFIGURE_OPTS="--with-wide-unicode" pyenv install -ks $dep_version
  pyenv local $dep_version
  export python_unicode_storage=`python -c "import sys; print('UCS4' if sys.maxunicode > 65536 else 'UCS2')"`

  if [ ! "$python_unicode_storage" = "UCS4" ] ; then
    pyenv uninstall -f $dep_version
    PYTHON_CONFIGURE_OPTS="--with-wide-unicode" pyenv install -k $dep_version
  fi
done
