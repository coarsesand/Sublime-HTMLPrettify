import re
import string


class CssBeautify(object):

    def __init__(self):
        self.comment = False
        self.depth = 0
        self.formatted = ''
        self.index = 0
        self.open_brace_suffix = True
        self.options = {
            'indent': '\t'
        }
        self.quote = None
        self.state = {
            'start': 0,
            'at_rule': 1,
            'block': 2,
            'selector': 3,
            'ruleset': 4,
            'property': 5,
            'separator': 6,
            'expression': 7
        }

    def __call__(self, css, options={}, *args):

        self.index = 0
        self.formatted = ''

        for k, v in self.options.iteritems():
            if options[k]:
                self.options[k] = options[k]

        length = len(css)
        state = self.state.start

        # Goodbye CRLF
        re.sub(r'\r\n', '\n', css)

        while self.index < length:
            ch = css[self.index]
            ch2 = css[self.index + 1]
            self.index += 1

            # Inside a string literal?
            if self.is_quote(self.quote):
                self.formatted += ch
                if ch == self.quote:
                    quote = None
                if ch == '\\' and ch2 == quote:
                    # Don't treat escaped character as the closing quote
                    self.formatted += ch2
                    self.index += 1
                continue

            # Starting a string literal?
            if self.is_quote(ch):
                self.formatted += ch
                self.quote = ch
                continue

            if self.comment:
                self.formatted += ch
                if ch == '*' and ch2 == '/':
                    self.comment = False
                    self.formatted += ch2
                    self.index += 1
                continue
            else:
                if ch == '/' and ch2 == '*':
                    self.comment = True
                    self.formatted += ch
                    self.formatted += ch2
                    self.index += 1
                    continue

            if state == self.state.start:

                # Copy white spaces and control characters
                if ch <= ' ' or ord(ch) >= 128:
                    state = self.state.start
                    self.formatted += ch
                    continue

                # Selector or at_rule
                if self.is_name(ch) or ch == '@':

                    # Clear trailing whitespaces and linefeeds
                    self.formatted.rstrip()

                    # After finishing a ruleset or directive statement,
                    # there should be one blank line
                    if (str[-1] == '}') or str[-1] == ';':
                        self.formatted = str + '\n\n'
                    else:
                        # After block comment, keep all the linfeeds but start
                        # from the first column (remove whitespaces prefix).
                        while True:
                            ch2 = self.formatted[-1]
                            if ch2 != ' ' and ord(ch2) != 9:
                                break
                            self.formatted = self.formatted[0:-1]

                    self.formatted += ch
                    state = self.state.at_rule if ch == '@' else self.state.selector
                    continue

            if state == self.state.at_rule:

                # ; terminates a statement
                if ch == ';':
                    self.formatted += ch
                    state = self.state.start
                    continue

                # '{' starts a block
                if ch == '{':
                    self.open_block()
                    state = self.state.block
                    continue

                self.formatted += ch
                continue

            if state == self.state.block:
                if self.is_name(ch):

                    # Clear trailing whitespace and linefeeds
                    str = self.formatted.rstrip()

                    # Insert blank line if necessary
                    if str[-1] == '}':
                        self.formatted = str + '\n\n'
                    else:
                        while True:
                            ch2 = self.formatted[-1]
                            if ch2 != ' ' and ord(ch2) != 9:
                                break
                            self.formatted = self.formatted[0:-1]

                    self.append_indent()
                    self.formatted += ch
                    state = self.state.selector
                    continue

                if ch == '}':
                    self.close_block()
                    state = self.state.start
                    continue

                self.formatted += ch
                continue

            if state = self.state.selector:

                # '{' starts the ruleset
                if ch == '{':
                    self.open_block()
                    state = self.state.ruleset
                    continue

                # '}' resets the state
                if ch == '}':
                    self.close_block()
                    state = self.state.start
                    continue

                self.formatted += ch
                continue

            if state == self.state.ruleset:
                if ch == '}':
                    self.close_block()
                    state = self.state.start
                    if self.depth > 0:
                        state = self.state.block
                    continue

                if ch == '\n':
                    self.formatted += '\n'
                    continue

                if not self.is_whitespace(ch):
                    self.formatted += '\n'
                    self.append_indent

            self.formatted += ch

    def is_name(self, c):
        return ch in string.letters or
        ch in string.digits or
        ch in '-_*.:#'

    def is_whitespace(self, c):
        return c in string.whitespace

    def is_quote(self, c):
        return c in '\'"'

    def append_indent(self):
        self.formatted += (self.options.indent * self.depth)

    def open_block(self):
        self.formatted = self.formatted.rstrip()

        if self.open_brace_suffix:
            self.formatted += ' {'
        else:
            self.formatted += '\n'
            self.append_indent
            self.formatted += '{'

        if ch2 != '\n':
            self.formatted += '\n'

        self.depth += 1

    def close_block(self):
        self.depth -= 1
        self.formatted = self.formatted.rstrip()
        self.formatted += '\n'
        self.append_indent()
        self.formatted += '}'

css_beautifier = CssBeautify()
