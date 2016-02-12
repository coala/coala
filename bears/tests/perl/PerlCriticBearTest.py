from bears.perl.PerlCriticBear import PerlCriticBear
from bears.tests.LocalBearTestHelper import verify_local_bear
from coalib.misc.ContextManagers import prepare_file

good_file = """
#!/usr/bin/perl

# $Id$
# $Revision$
# $Date$

use strict;
use warnings;
use vars qw/ $VERSION /;

$VERSION = '1.00';

exit 1 if !print "Hello, world!\n";
""".split("\n")


bad_file = """
#!/usr/bin/perl

print "Hello World\n";
""".split("\n")


config_file = """
severity  = 5
# for signatures
[-Subroutines::ProhibitSubroutinePrototypes]

[TestingAndDebugging::RequireUseStrict]

[TestingAndDebugging::RequireUseWarnings]
""".split("\n")


PerlCriticBear1Test = verify_local_bear(PerlCriticBear,
                                        valid_files=(good_file,),
                                        invalid_files=(bad_file,))


with prepare_file(config_file,
                  filename=None,
                  force_linebreaks=True,
                  create_tempfile=True) as (conf_lines, conf_file):
    PerlCriticBear2Test = verify_local_bear(PerlCriticBear,
                                            valid_files=(bad_file),
                                            invalid_files=(),
                                            settings={
                                                "perlcritic_config": conf_file})
