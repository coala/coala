"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""


class Setting:
    def __init__(self, key, value, comments_before=None, trailing_comment=''):
        """
        :param key: original key
        :param value: original value (string)
        :param comments_before: comments without preceding #
        :param trailing_comment: without preceding #
        :return:
        """
        if comments_before is None:
            comments_before = []

        self.key = key
        self.value = value
        self.comments_before = comments_before
        self.trailing_comment = trailing_comment

    def generate_lines(self):
        """
        :return: a list of lines representing this setting including comments
        """
        result = []
        for comment in self.comments_before:
            if comment is not None:
                if comment:
                    result.append('# '+comment)
                else:
                    result.append('')

        if self.key == '':
            return result

        line = self.key + ' = ' + self.value

        if self.trailing_comment:
            line += ' # ' + self.trailing_comment

        result.append(line)
        return result