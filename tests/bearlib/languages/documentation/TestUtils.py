import os


def load_testdata(filename):
    filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)),
        os.path.join('documentation_extraction_testdata',
                     filename))

    with open(filename) as test_file:
        data = test_file.read()

    return data.splitlines(keepends=True)
