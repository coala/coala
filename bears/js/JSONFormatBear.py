import json
from collections import OrderedDict

from coalib.bearlib.abstractions.CorrectionBasedBear import CorrectionBasedBear
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.results.Result import Result


class JSONFormatBear(CorrectionBasedBear):
    try:
        DecodeError = json.decoder.JSONDecodeError
    except:
        DecodeError = ValueError

    GET_REPLACEMENT = lambda self, **kwargs: self.get_plain_json(**kwargs)
    RESULT_MESSAGE = ("This file can be reformatted by sorting keys and "
                      "following indentation.")

    @staticmethod
    def get_plain_json(file, json_sort, indent):
        json_content = json.loads(''.join(file), object_pairs_hook=OrderedDict)
        new_file = json.dumps(json_content,
                              indent=indent,
                              sort_keys=json_sort).splitlines(True)

        # Because of a bug in several python versions we have to correct
        # whitespace here.
        return [line.rstrip(" \n")+"\n" for line in new_file], []

    def run(self,
            filename,
            file,
            json_sort: bool=False,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH):
        """
        Raises issues for any deviations from the pretty-printed JSON.

        :param json_sort: Whether or not keys should be sorted.
        :param tab_width: Number of spaces to indent.
        """
        try:
            for result in self.retrieve_results(filename,
                                                file,
                                                json_sort=json_sort,
                                                indent=tab_width):
                yield result
        except self.DecodeError as err:
            yield Result.from_values(
                self,
                "This file does not contain parsable JSON. '{adv_msg}'"
                .format(adv_msg=str(err)),
                file=filename)
