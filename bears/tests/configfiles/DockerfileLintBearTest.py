from bears.configfiles.DockerfileLintBear import DockerfileLintBear
from bears.tests.LocalBearTestHelper import verify_local_bear


good_file = """
FROM ubuntu:14.04

# Install basic tools
RUN apt-get -y -qq update
RUN apt-get -y -qq upgrade
""".split("\n")


bad_file = """
FROM ubuntu:14.04

# Install basic tools
apt-get -y -qq update
apt-get -y -qq upgrade
""".split("\n")


DockerfileLintBear1Test = verify_local_bear(DockerfileLintBear,
                                            valid_files=(good_file,),
                                            invalid_files=(bad_file,))
