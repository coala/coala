from xml.etree import ElementTree

from coalib.bearlib.abstractions.CorrectionBasedBear import CorrectionBasedBear
from coalib.results.Result import Result


def indent(elem, indentation=2, level=0):
    ind = "\n" + level*indentation*" "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = ind + indentation*" "
        if not elem.tail or not elem.tail.strip():
            elem.tail = ind
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = ind
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = ind


class XMLFormatBear(CorrectionBasedBear):
    GET_REPLACEMENT = lambda self, **kwargs: self.get_plain_xml(**kwargs)
    RESULT_MESSAGE = "This file can be cleanly indented."

    @staticmethod
    def get_plain_xml(file):
        xml = ElementTree.fromstringlist(file)
        indent(xml.getroot())
        return ElementTree.tostring(xml).splitlines(True), []


    def run(self, filename, file):
        """
        Raises issues for any deviations from the pretty-printed JSON.

        :param json_sort: Whether or not keys should be sorted.
        :param indent:    Number of spaces to indent.
        """
        try:
            for result in self.retrieve_results(filename, file):
                yield result
        except self.DecodeError as err:
            yield Result.from_values(
                self,
                "This file does not contain parsable JSON. '{adv_msg}'"
                .format(adv_msg=str(err)),
                file=filename)
