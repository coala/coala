"""
A ResultAction is an action that is applicable to at least some results. This
file serves the base class for all result actions, thus providing a unified
interface for all actions.
"""
from coalib.settings.FunctionMetadata import FunctionMetadata
from coalib.settings.Section import Section


class ResultAction:
    @staticmethod
    def is_applicable(result):
        """
        Checks whether the Action is valid for the result type.

        :param result: The result from the coala run to check if an Action is
                       applicable.
        """
        return False

    def apply(self, result, original_file_dict, file_diff_dict, **kwargs):
        """
        This action has no description although it should. Probably something
        went wrong.
        """
        raise NotImplementedError

    def apply_from_section(self,
                           result,
                           original_file_dict,
                           file_diff_dict,
                           section):
        """
        Applies this action to the given results with all additional options
        given as a section. The file dictionaries
        are needed for differential results.

        :param result:             The result to apply.
        :param original_file_dict: A dictionary containing the files in the
                                   state where the result was generated.
        :param file_diff_dict:     A dictionary containing a diff for every
                                   file from the state in the
                                   original_file_dict to the current state.
                                   This dict will be altered so you do not
                                   need to use the return value.
        :param section:            The section where to retrieve the additional
                                   information.
        :return                    The modified file_diff_dict.
        """
        if not isinstance(section, Section):
            raise TypeError("section has to be of type Section.")
        if not isinstance(original_file_dict, dict):
            raise TypeError("original_file_dict has to be of type dict.")
        if not isinstance(file_diff_dict, dict):
            raise TypeError("file_diff_dict has to be of type dict.")

        params = self.get_metadata().create_params_from_section(section)
        return self.apply(result, original_file_dict, file_diff_dict, **params)

    @classmethod
    def get_metadata(cls):
        """
        Retrieves metadata for the apply function. The description may be used
        to advertise this action to the user. The parameters and their help
        texts are additional information that are needed from the user. You can
        create a section out of the inputs from the user and use
        apply_from_section to apply

        :return A FunctionMetadata object.
        """
        data = FunctionMetadata.from_function(
            cls.apply,
            omit={"self", "result", "original_file_dict", "file_diff_dict"})
        data.name = cls.__name__

        return data
