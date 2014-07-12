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
from coalib.fillib.misc.i18n import _


class StringConstants:
    THIS_IS_A_BUG = _("This is a bug. We are sorry for the inconvenience. "
                   "Please contact the developers if this happens more than once.")
    """
    Strings which may be interpreted as 'True' (some english values will be accepted in addition to the translated
    ones since they are quite usual.) If there is no suitable translation, repeat one of the previous translations and
    the value will be ignored. It is irrelevant which original is translated witch witch translation. Mind that all
    strings here have to be lower case!
    """
    TRUE_STRINGS = ['1', _("on"), 'y', _("y"), 'yes', _("yes"), _("yeah"), _("sure"), 'true', _("true"),
                    _('definitely'), _('yup')]

    """
    Strings which may be interpreted as 'False' (some english values will be accepted in addition to the translated
    ones since they are quite usual.) If there is no suitable translation, repeat one of the previous translations and
    the value will be ignored. It is irrelevant which original is translated witch witch translation. Mind that all
    strings here have to be lower case!
    """
    FALSE_STRINGS = ['0', _('off'), 'n', _("n"), 'no', _("no"),  _('nope'), _('nah'),  'false', _("false")]
