import multiprocessing
from coalib.bears.Bear import Bear
from coalib.settings.Section import Section


class BadTestBear(Bear):

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    def run(self):
        raise NotImplementedError


class TestBear(Bear):

    BEAR_DEPS = {BadTestBear}

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    def run(self):
        self.print('set', 'up', delimiter='=')
        self.err('teardown')
        self.err()

links = {'link1': 'https://oss.sonatype.org/content/repositories/releases/org/scalastyle/scalastyle_2.10/0.8.0/scalastyle_2.10-0.8.0-batch.jar',
         'link2': 'http://sourceforge.net/projects/checkstyle/files/checkstyle/6.15/checkstyle-6.15-all.jar',
         'link3': 'https://raw.githubusercontent.com/noveogroup/android-check/master/android-check-plugin/src/main/resources/checkstyle/checkstyle-easy.xml',
         'link4': 'https://raw.githubusercontent.com/noveogroup/android-check/master/android-check-plugin/src/main/resources/checkstyle/checkstyle-hard.xml',
         'link5': 'http://geosoft.no/development/geosoft_checks.xml'}


queue = multiprocessing.Queue()
settings = Section('main')
bear = TestBear(settings, queue)
for link in links:
    print('link')
    bear.download_cached_file(links[link], link)
