class FunctionHelper:

    def __init__(self, name, param_list, descr=None):
        self.name = name
        self.param_list = param_list
        self.function_descr = descr

    def add_param(self, param):
        self.param_list.append(param)

    def get_function_params(self):
        return self.param_list

    def get_function_name(self):
        return self.name

    def get_dict(self):
        dictionary = {}
        dictionary['name'] = self.name
        dictionary['params'] = self.param_list
        return dictionary