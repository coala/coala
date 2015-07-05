import time
import datetime
from gettext import ngettext

from coalib.misc.i18n import _


def process_timestamp(timestamp, reference_time):
    timediff = (time.mktime(reference_time)-time.mktime(timestamp))
    d = datetime.timedelta(seconds=timediff)
    if int(d.seconds/60) < 1:
        return _("Just Now")
    if int(d.seconds/3600) <= 1:
        minutes = int(d.seconds/60)
        return ngettext("A minute", "{minutes} minutes",
                        minutes).format(minutes=minutes)
    if int(d.seconds/3600) <= 12:
        hours = int(d.seconds/3600)
        return ngettext("An hour", "{hours} hours", hours).format(hours=hours)
    if int(d.days * 24 + d.seconds/3600) <= reference_time.tm_hour:
        return _("Today")
    if d.days == 1:
        return _("Yesterday")
    if d.days <= 7:
        return _(time.strftime("%A", timestamp))
    if d.days < 14:
        return str(int(d.days / 7)) + _(" week ago")
    if d.days <= reference_time.tm_yday:
        return _(time.strftime("%B", timestamp))
    else:
        return _(time.strftime("%Y", timestamp))
