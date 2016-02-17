import re
import requests

from coalib.results.Diff import Diff
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


class InvalidLinkBear(LocalBear):

    @classmethod
    def check_prerequisites(cls):
        code = InvalidLinkBear.get_status_code_or_error("http://www.google.com")
        return ("You are not connected to the internet."  # pragma: no cover
                if code is None else True)

    @staticmethod
    def get_status_code_or_error(url):
        try:
            code = requests.head(url, allow_redirects=False).status_code
            return code
        except requests.exceptions.RequestException:
            pass

    @staticmethod
    def find_links_in_file(file):
        regex = re.compile(
            r'((ftp|http)s?:\/\/\S+\.(?:[^\s\(\)\'\>]+|'
            r'\([^\s\(\)]*\))*)(?<!\.)(?<!\,)')
        for line_number, line in enumerate(file):
            match = regex.search(line)
            if match:
                link = match.group()
                code = InvalidLinkBear.get_status_code_or_error(link)
                yield line_number + 1, link, code

    def run(self, filename, file):
        '''
        Yields results for all invalid links in a file.
        '''
        for line_number, link, code in InvalidLinkBear.find_links_in_file(file):
            if code is None:
                yield Result.from_values(
                    origin=self,
                    message='Broken link - unable to connect to this url.',
                    file=filename,
                    line=line_number,
                    severity=RESULT_SEVERITY.MAJOR)
            elif not 200 <= code < 300:
                if 400 <= code < 600:  # HTTP status 40x or 50x
                    yield Result.from_values(
                        origin=self,
                        message='Broken link - unable to connect to this url.' +
                                ' (HTTP Error: {code})'.format(code=code),
                        file=filename,
                        line=line_number,
                        severity=RESULT_SEVERITY.NORMAL)
                if 300 <= code < 400:  # HTTP status 30x
                    redirect_url = requests.head(link, allow_redirects=True).url
                    diff = Diff(file)
                    current_line = file[line_number - 1]
                    start = current_line.find(link)
                    end = start + len(link)
                    replacement = current_line[:start] + \
                        redirect_url + current_line[end:]
                    diff.change_line(line_number, current_line, replacement)

                    yield Result.from_values(
                        self,
                        'This link redirects to ' + redirect_url,
                        diffs={filename: diff},
                        file=filename,
                        line=line_number,
                        severity=RESULT_SEVERITY.NORMAL)
