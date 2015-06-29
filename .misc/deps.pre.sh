set -x
set -e

# Disable things that circleci starts that we do not need
sudo service mysql stop
sudo service mongodb stop
sed -i '/source \/home\/ubuntu\/virtualenvs\//d' ~/.circlerc

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 0) dep_versions=( "pypy3-2.4.0" "3.2.6" "3.3.6" "3.4.2" ) ;;
 1) dep_versions=( "3.3.6" ) ;;
 2) dep_versions=( "3.2.6" ) ;;
 3) dep_versions=( "pypy3-2.4.0" ) ;;
 *) dep_versions=( "3.4.2" ) ;;
esac

# Install python version needed
for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
done

pyenv local ${dep_versions[-1]}
