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
        self.indent_stack = []

    def pop_indent(self):
        """
        Pop last indent.
        """
        if self.indent_stack:
            self.indent_stack.pop()

    def push_indent(self, indent):
        """
        Push indent.

        :param indent: Indent
        """
        self.indent_stack.append(indent)

    def get_current_indent(self):
        """
        Combine all indents to get current indent.

        :return: Current indent
        """
        return "".join(self.indent_stack)

    def indent_new_lines(self, text):
        """
        Indent all the lines except first one.

        :param text: Text to indent
        :return: Indented text
        """
        lines = text.splitlines()
        lines[1:] = [self.get_current_indent() + x if x.strip() != "" else "" for x in lines[1:]]
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
