Adding CI to your Fork
======================

This tutorial will help you add the CI tools, that are used in
coala repositories to test the code, to your forked repository.
We recommend you to add all the CI and test everything in your
own repository before doing a PR.

Before we start adding CI it's important you have a GitHub account
and know how to fork repositories. In case you don't, you should
have a look into our `Git Tutorial <https://coala.io/gitbasics>`_.

Travis CI
---------

Travis is used to confirm that the tools install and build
properly. It also runs the tests and confirms all test cases
pass and have 100% coverage. These are examples of travis CI
checks used in coala and coala-bears repository:
https://travis-ci.org/coala/coala/ and
https://travis-ci.org/coala/coala-bears/.
To run identical CI checks in travis you will need to configure your
forked repository and to do that follow the steps mentioned below.

1. Go to `travis-ci.org <https://travis-ci.org/>`_ and create
   an account. You can simply use your GitHub account for that.
2. On the top left corner you will see a "+" icon beside
   "My Repositories". Click on that, and it will take you to
   your travis-ci profile.
3. Sync your account with github by clicking on the top right
   button saying "Sync account".
4. Find the forked coala repository in the list and enable builds
   for it.
5. Travis CI requires a .travis.yml file containing the settings
   and build instructions, e.g `coala's .travis.yml
   <https://github.com/coala/coala/blob/master/.travis.yml>`_.
   Your forked repository from coala will already have that file.
6. Watch the builds at
   travis-ci.org/<username>/<repository>/builds.

AppVeyor CI
-----------

To find out how coala acts in Microsoft Windows, we use
AppVeyor which runs test and build commands in a
Microsoft Windows box. Here are examples of CI build in AppVeyor :
https://ci.appveyor.com/project/coala/coala/ and
https://ci.appveyor.com/project/coala/coala-bears/.
Now to add an indentical Appveyor CI to your forked repository,
follow the following instructions.

1. Go to `ci.appveyor.com <http://ci.appveyor.com>`_ and login
   using your GitHub account.
2. Click on "New Project" and find forked repository from the
   repositories listed under your username.
3. On the right side, you will see an "Add" button, click on it
   and it will add it to your projects.
4. AppVeyor CI requires appvyor.yml file that should have the
   settings and instructions for windows, e.g `coala's appveyor.yml
   <https://github.com/coala/coala/blob/master/.misc/appveyor.yml>`_.
   Your forked repository already has that file.
5. In case it has a different name or not in the root directory you
   have to configure it in the settings which can be found at
   ci.appveyor.com/project/<username>/<repository>/settings.
   For coala's repository the appveyor.yml file is inside the .misc
   directory. So you have to go to Settings and under
   "Custom configuration .yml file name", enter
   :code:`.misc/appveyor.yml`. For coala-bears's repository the
   the appveyor.yml file is in the .ci directory. So you have to
   enter :code:`.ci/appveyor.yml`. If you have forked a different
   repository, enter the right .yml file path for that.
6. In coala, the appveyor.yml sets the setting to only build
   from the master branch, however in your fork you may want it
   to build other branches as well. You can do that by configuring
   "Branches to Build" in Settings, so there will be no need to
   change the file for that.
7. From now on appveyor will run the builds for every commit you
   push, which you can watch at
   ci.appveyor.com/project/<username>/<repository>.
   You can also start a build by yourself by clicking on "New Build"

Circle CI
---------

Circle CI is also used for the same purpose as travis, to
check everything installs and builds properly, and also to run
the tests. Here are examples of checks in circle CI :
https://circleci.com/gh/coala/coala/ and
https://circleci.com/gh/coala/coala-bears/. To add these CI builds
to your forked repositories follow the instructions here.

1. Go to `circleci.com <https://circleci.com>`_ and sign up using
   your GitHub account.
2. After signing up it will take you to the dashboard which lists
   the project that already use circle and which don't. By default
   it selects all the repositories, but if you want you can deselect
   them and only choose the forked repository.
3. Then click the "Follow and Build" button.
4. In project settings go to Adjust Parallelism under Build Settings
   and enable a second container by clicking on the box with "2x".
5. Using a circle.yml file it runs the builds. e.g
   `coala's circle.yml
   <https://github.com/coala/coala/blob/master/circle.yml>`_.
   Your forked repository from coala will already have that file.
6. You can then watch the builds at
   circleci.com/gh/<username>/<repository>.
7. In project settings go to Build Environments under Build Settings.
   You will see by default the OS used for builds is Trusty one,
   however we recommend using Precise as its faster.

Codecov
-------

We require 100% test coverage, and to test that we use
`codecov.io <https://codecov.io>`_ which takes data from all other
CI to confirm its coverage.
Here are two example reports from coala and coala-bears repository :
https://codecov.io/gh/coala/coala/ and
https://codecov.io/gh/coala/coala-bears/. Once you follow the
instructions here, you will have identical reports for your forked
repository.

1. Go to `codecov.io <https://codecov.io>`_ and sign up using your
   GitHub account.
2. Click on your username, and that will take you to a page where
   the repositories that use codecov are listed.
3. Click on "Add new repository" and it will take you to a page that
   lists all your repositories. Choose the forked repository for
   which you want to enable codecov.
4. Like other CI, this also has a configuration file, .codecov.yml
   file which your forked repository will already have. e.g
   `coala's .codecov.yml
   <https://github.com/coala/coala/blob/master/.codecov.yml>`_
   The CI uploads the test reports to codecov, which then creates
   an overall coverage report.
5. You can watch the reports at codecov.io/gh/<username>/<repository>
