import sys
from coalib.misc import Constants


__version__ = Constants.VERSION


# unnecessary space




def assert_supported_version():  # pragma: no cover
    if not sys.version_info > (3, 2):
        print("coala supports only python 3.3 or later.")
        exit(4)



#### RANDOME LONG LINE ###############################################################################################################################

# Extra space at end of line                               
# Extra newlines at end




