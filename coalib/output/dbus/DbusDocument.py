import os
import dbus.service

from coalib.processes.SectionExecutor import SectionExecutor
from coalib.settings.SectionManager import SectionManager
from coalib.output.ClosableObject import ClosableObject


class DbusDocument(dbus.service.Object):
    """
    This is a dbus object-path for every document that a DbusApplication wants
    coala to analyze.
    """
    interface = "org.coala.v1"

    def __init__(self, path=""):
        super(DbusDocument, self).__init__()
        if path:
            abs_path = os.path.abspath(path)
            self._path = abs_path
        else:
            self._path = ""

    @dbus.service.method(interface,
                         in_signature="",
                         out_signature="a(a(sssuq)a(sssuq))")
    def Analyze(self):
        """
        This method analyzes the document and sends back the result

        :return: A list containing two tuples, one for global bears and the
                 other for local bears. The tuple contains the information
                 about the result in the order - (str)origin, (str)message,
                 (str)file_path, (uint32)line_number, (uint16)severity
        """
        retval = []
        if self._path == "":
            return retval

        args = ["--output=none", "--file=" + self.path]
        sections, local_bears, global_bears, targets, interactor, log_printer \
            = SectionManager().run(arg_list=args)
        for section_name in sections:
            section = sections[section_name]
            if not section.is_enabled(targets):
                continue
            yielded_result = SectionExecutor(
                section=section,
                global_bear_list=global_bears[section_name],
                local_bear_list=local_bears[section_name],
                interactor=interactor,
                log_printer=log_printer).run()
            if yielded_result[0]:
                retval.append(
                    DbusDocument.results_to_dbus_struct(yielded_result)
                )

        if log_printer is not None and isinstance(log_printer, ClosableObject):
            log_printer.close()
        if interactor is not None and isinstance(interactor, ClosableObject):
            interactor.close()

        return retval

    @staticmethod
    def results_to_dbus_struct(res):
        return (
            (tuple(item) for sublist in res[1].values() for item in sublist),
            (tuple(item) for sublist in res[2].values() for item in sublist)
        )

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        new_abs_path = os.path.abspath(new_path)
        self._path = new_abs_path
