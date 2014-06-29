class OutputObject:

    def __init__(self, caption, lines=None):
        self.caption = caption
        self.lines = lines
        if not self.lines: self.lines = []
        self.string_representation = self.caption #TODO

    def __str__(self):
        self.update_string_representation()
        return self.string_representation

    def update_string_representation(self):
        str_repr = self.caption + "\n"
        for line in self.lines:
            str_repr += line.to_string(1)
        self.string_representation = str_repr

    def add_line(self, line):
        self.lines.append(line)

class OutputLine:
    def __init__(self):
        self.sublines = []
        self.elems = []

    def add_elem(self, string, color='\033[0m', position=None):
        new_elem = OutputElem(string, color, position)
        self.elems.append(new_elem)

    def append_elem(self, elem):
        self.elems.append(elem)

    def append_line(self, line):
        self.sublines.append(line)

    def to_string(self, indent):
        line_string = ""
        for i in range(len(self.elems)):
            elem_string = self.elems[i].color + self.elems[i].string + "\033[0m"
            if self.elems[i].position == None:
                line_string += elem_string
            elif self.elems[i].position < (len(line_string)-sum([len(elem.color)+len('\033[0m') for elem in self.elems[:i] if i > 0])):
                if i:
                    line_string = line_string[:self.elems[i].position + len(self.elems[i-1].color)] + elem_string
                else:
                    line_string = line_string[:self.elems[i].position] + elem_string
            else:
                line_string = line_string + " " * (self.elems[i].position - (len(line_string)-sum([len(elem.color)+len('\033[0m') for elem in self.elems[:i] if i > 0]))) + elem_string
        line_string = "\t" * indent + line_string + "\n"

        for subline in self.sublines:
            line_string += subline.to_string(indent+1)

        return line_string

class OutputElem:
    def __init__(self, string, color='\033[0m', position=None ):
        self.string = string
        self.color = color
        if position != None:
            assert isinstance(position, int)
            assert position >= 0
        self.position = position
