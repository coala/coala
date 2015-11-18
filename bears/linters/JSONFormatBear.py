from collections import OrderedDict
import json

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.Diff import Diff


class JSONFormatBear(LocalBear):
    try:
        DecodeError = json.decoder.JSONDecodeError
    except:
        DecodeError = ValueError

    def run(self, filename, file, json_sort: bool=False, indent: int=4):
        """
        Raises issues for any deviations from the pretty-printed JSON.

        :param json_sort: Whether or not keys should be sorted.
        :param indent:    Number of spaces to indent.
        """
        try:
            content = ''.join(file)
            json_content = json.loads(content, object_pairs_hook=OrderedDict)
            new_file = json.dumps(json_content,
                                  indent=indent,
                                  sort_keys=json_sort).splitlines(True)
            # Because of a bug we have to strip whitespaces
            new_file = [line.rstrip(" \n")+"\n" for line in new_file]
            if file != new_file:
                wholediff = Diff.from_string_arrays(file, new_file)

                for diff in wholediff.split_diff():
                    yield Result(
                        self,
                        "This file can be reformatted by sorting keys and "
                        "following indentation.",
                        affected_code=(diff.range(filename),),
                        diffs={filename: diff})
        except self.DecodeError as err:
            yield Result.from_values(
                self,
                "This file does not contain parsable JSON. '{adv_msg}'"
                .format(adv_msg=str(err)),
                file=filename)
