set -x
set -e

# Disable things that circleci starts that we do not need
sudo service mysql stop
sudo service mongodb stop
sed -i '/source \/home\/ubuntu\/virtualenvs\//d' ~/.circlerc
