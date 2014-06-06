__author__ = 'Fabian Neuschmidt, Lasse Schuirmann'


class ColorPrinter:
    @staticmethod
    def print(color, *args, delimiter=' ', end='\n'):
        """
        prints arguments in specified color

        :color: Color in which the following arguments should be printed
        :*args: Any Number of Arguments, preferably strings or numbers
        :returns: None

        """
        try:
            print('\033[' + color.value + 'm', end='')
            for arg in args:
                print(arg, end=delimiter)
            print('\033[0m', end=end)
        except:
            for arg in args:
                print(arg, end=delimiter)
            print(end=end)
