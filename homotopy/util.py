import re


class IndentManager:
    """
    Helper for managing indent.
    """
    def __init__(self, base_indent=""):
        """
        Initializer.

        :param base_indent: Base indent
        """
        self.base_indent = base_indent

    @staticmethod
    def indent_new_lines(text, indent):
        """
        Indent all the lines except first one.

        :param text: Text to indent
        :param indent: Indent text
        :return: Indented text
        """
        lines = text.splitlines()
        lines[1:] = [indent + x if x.strip() != "" else "" for x in lines[1:]]
        return "\n".join(lines)

    def indent_base(self, text):
        """
        Indent all lines with base indent.

        :param text: Text to indent
        :return: Indented text
        """
        lines = text.splitlines()
        lines = [self.base_indent + x if x.strip() != "" else "" for x in lines]
        return "\n".join(lines)

    def take_base_indent(self, line):
        """
        Take base indent.

        :param line: Line text
        :return: Line without the indent
        """
        m = re.match(r"^[\t ]*", line)
        self.base_indent = m.group()

        return line[m.end():]


class ContextManager:
    """
    Class for managing substituted parameters to be used again.
    """
    def __init__(self):
        """
        Initialize stack.
        """
        self.stack = []

    def new_scope(self):
        """
        Add new scope.
        """
        self.stack.append({})

    def remove_scope(self):
        """
        Remove last scope.
        """
        if self.stack:
            self.stack.pop()

    def add_variable(self, name, value):
        """
        Add variable to current scope.

        :param name: Variable name
        :param value: Variable value
        """
        if self.stack:
            self.stack[-1][name] = value
        else:
            raise Exception("No scope to add variable to")

    def __getitem__(self, item):
        """
        Get variable from last scope.

        :param item: Variable name
        :return: Variable value if it exists. Empty string otherwise
        """
        i = 2
        while i <= len(self.stack):
            if item in self.stack[-i]:
                return self.stack[-i][item]

            i += 1

        return ""
