import datetime
import sys
import unittest

sys.path.insert(0, ".")
from coalib.output.gui.support.Timestamp import process_timestamp
from coalib.misc.i18n import _


class Timestamp(unittest.TestCase):
    def test_process_timestamp(self):
        reference_timestamp = datetime.datetime(
            2015, 7, 3, 20, 30, 0).timetuple()
        self.assertEqual(_("Just Now"), process_timestamp(reference_timestamp,
                                                          reference_timestamp))
        timestamp = datetime.datetime(2014, 7, 1, 0, 0, 0).timetuple()
        self.assertEqual("2014", process_timestamp(timestamp,
                                                   reference_timestamp))
        timestamp = datetime.datetime(2015, 7, 1, 0, 0, 0).timetuple()
        self.assertEqual(_("Wednesday"),
                         process_timestamp(timestamp, reference_timestamp))
        timestamp = datetime.datetime(2015, 6, 1, 0, 0, 0).timetuple()
        self.assertEqual(_("June"), process_timestamp(timestamp,
                                                      reference_timestamp))
        timestamp = datetime.datetime(2015, 7, 3, 15, 0, 0).timetuple()
        self.assertEqual(_("5 hours"), process_timestamp(timestamp,
                                                         reference_timestamp))
        timestamp = datetime.datetime(2015, 7, 3, 20, 29, 0).timetuple()
        self.assertEqual(_("A minute"),
                         process_timestamp(timestamp, reference_timestamp))
        timestamp = datetime.datetime(2015, 7, 3, 20, 0, 0).timetuple()
        self.assertEqual(_("30 minutes"),
                         process_timestamp(timestamp, reference_timestamp))
        timestamp = datetime.datetime(2015, 7, 2, 0, 0, 0).timetuple()
        self.assertEqual(_("Yesterday"),
                         process_timestamp(timestamp, reference_timestamp))
        timestamp = datetime.datetime(2015, 7, 3, 0, 0, 0).timetuple()
        self.assertEqual(_("Today"),
                         process_timestamp(timestamp, reference_timestamp))
        timestamp = datetime.datetime(2015, 6, 23, 0, 0, 0).timetuple()
        self.assertEqual(_("1 week ago"),
                         process_timestamp(timestamp, reference_timestamp))



if __name__ == '__main__':
    unittest.main(verbosity=2)
