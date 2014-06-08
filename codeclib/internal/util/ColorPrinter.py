__author__ = 'Fabian Neuschmidt, Lasse Schuirmann'


class ColorPrinter:
    def __init__(self):
        pass

    @staticmethod
    def putout(color, *args, delimiter=' ', end='\n'):
        """
        prints arguments in specified color

        :color: Color in which the following arguments should be printed
        :*args: Any Number of Arguments, preferably strings or numbers
        :returns: None

        """
        color_code_dict = {
            'black': '0;30', 'bright gray': '0;37',
            'blue': '0;34', 'white': '1;37',
            'green': '0;32', 'bright blue': '1;34',
            'cyan': '0;36', 'bright green': '1;32',
            'red': '0;31', 'bright cyan': '1;36',
            'purple': '0;35', 'bright red': '1;31',
            'yellow': '0;33', 'bright purple': '1;35',
            'dark gray': '1;30', 'bright yellow': '1;33',
            'normal': '0',
        }
        try:
            print('\033[' + color_code_dict.get(color, '0') + 'm', end='')
            for arg in args:
                print(arg, end=delimiter)
            print('\033[0m', end=end)
        except:
            for arg in args:
                print(arg, end=delimiter)
            print(end=end)
