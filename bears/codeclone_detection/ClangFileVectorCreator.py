import copy


from bears.codeclone_detection.ClangCountVectorCreator import (
    ClangCountVectorCreator)
from bears.codeclone_detection.FunctionHelper import FunctionHelper
from bears.codeclone_detection.ClangCountingConditions import (
    get_identifier_name,
    is_function_declaration)
from coalib.bearlib.parsing.clang.cindex import Cursor, Index, CursorKind
from bears.codeclone_detection.CloneDetectionRoutines import add_count_vectors


class ClangFileVectorCreator:
    def __init__(self, conditions=None, weightings=None):
        self.conditions = conditions
        self.weightings = weightings
        self.count_vectors = {}
        self.stack = []
        self.function_dict = {}
        self.function_mapping_dict = {}
        self.function_vectors = {}
        self.function_vectors_before_merge = {}

    def _create_function_list(self, cursor, filename):
        assert isinstance(cursor, Cursor)
        file = cursor.location.file
        if file is not None:
            file = file.name.decode()

        if str(file) == str(filename) and is_function_declaration(cursor):
            function_name = get_identifier_name(cursor)
            function_name = function_name[0:function_name.find('(')]
            function_args = list(cursor.get_arguments())
            func_def = get_identifier_name(cursor)[:-1]
            func_def_list = func_def.split(",")
            func_descr = ''
            for ele, fele in zip(function_args, func_def_list):
                literal = ele.spelling.decode('utf-8')
                func_descr += (fele+literal)
            if func_descr == '':
                func_descr += func_def_list[0]
            func_descr += ')'
            decoded_function_args = []
            for arg in function_args:
                decoded_function_args.append(arg.spelling.decode('utf-8'))
            function = FunctionHelper(function_name,
                                      decoded_function_args,
                                      (cursor.extent.start.line, func_descr))
            self.function_dict[function_name] = function
            self._create_function_call_list(cursor, function_name)
        else:
            for child in cursor.get_children():
                self._create_function_list(child, filename)

    def _create_function_call_list(self,
                                   cursor,
                                   calling_function,
                                   child_num=0):
        assert isinstance(cursor, Cursor)
        self.stack.append((cursor, child_num))
        called_function = get_identifier_name(cursor)
        # print("called" + str(name) + str(cursor.kind))
        if cursor.kind == CursorKind.CALL_EXPR:
            function_args = []
            for i, child in enumerate(cursor.get_children()):
                if called_function != get_identifier_name(child):
                    if get_identifier_name(child) == '':
                        function_args.append(0)
                    else:
                        function_args.append(get_identifier_name(child))

            function = FunctionHelper(called_function, function_args)
            self._update_function_mapping_dict(calling_function, function)

        for i, child in enumerate(cursor.get_children()):
            self._create_function_call_list(child, calling_function, i)

        self.stack.pop()

    def _update_function_mapping_dict(self,
                                      calling_function,
                                      called_function_mapping):

        if calling_function in self.function_mapping_dict.keys():
            function_mapping_list = self.function_mapping_dict[
                calling_function]
            function_mapping_list.append(called_function_mapping)
        else:
            function_mapping_list = [called_function_mapping]

        self.function_mapping_dict[calling_function] = function_mapping_list

    def get_vectors_for_file(self, filename, include_paths=()):
        args = ["-I"+path for path in include_paths]
        root = Index.create().parse(filename, args=args).cursor
        self._create_function_list(root, filename)
        cvs = ClangCountVectorCreator(self.conditions, self.weightings)
        self.function_vectors = cvs.get_vectors_for_file(filename,
                                                         include_paths)
        self.function_vectors_before_merge = copy.deepcopy(
            self.function_vectors)
        self.combine_vectors()

    def combine_vectors(self, entry_point="main"):
        if entry_point in self.function_mapping_dict:
            calling_function = self.function_dict[entry_point]
            cvs_calling_function = self.function_vectors[
                calling_function.function_descr]
            calling_function_list = self.function_mapping_dict[entry_point]
            for called_function in calling_function_list:
                if (called_function.get_function_name() not in
                        self.function_dict):
                    continue
                self.combine_vectors(called_function.get_function_name())
                function_declaration = self.function_dict[
                    called_function.get_function_name()]
                cvs_declaration = self.function_vectors[
                    function_declaration.function_descr]
                for var_dcl, var_call in zip(
                        function_declaration.get_function_params(),
                        called_function.get_function_params()):
                    cvs_calling_function[var_call] = add_count_vectors(
                        cvs_calling_function[var_call],
                        cvs_declaration[var_dcl])



