# DO NOT TOUCH UNLESS YOU'RE 100% SURE WHAT YOU'RE DOING!

class CommandParam:
    is_optional = False

    def get_regex(self):
        pass

    def get_name(self):
        pass


class Const(CommandParam):
    def __init__(self, name, is_optional=False):
        self.name = name
        self.is_optional = is_optional
        if " " in name:
            raise Exception("One or more spaces found in command param '%s'." % name)

    def get_regex(self):
        regex = r"(\s+" + self.name + ")"
        return regex + ("?" if self.is_optional else "")

    def get_name(self):
        if self.is_optional:
            return "[" + self.name + "]"
        else:
            return self.name

    def process_matches(self, params):
        val = params.pop(0)
        if val is None:
            return None
        else:
            return val.lstrip()


class Int(CommandParam):
    def __init__(self, name, is_optional=False):
        self.name = name
        self.is_optional = is_optional
        if " " in name:
            raise Exception("One or more spaces found in command param '%s'." % name)

    def get_regex(self):
        regex = r"(\s+[0-9]+)"
        return regex + ("?" if self.is_optional else "")

    def get_name(self):
        if self.is_optional:
            return "[%s]" % self.name
        else:
            return "%s" % self.name

    def process_matches(self, params):
        val = params.pop(0)
        if type(val) == int:
            return val
        if val is None:
            return None
        else:
            return int(val.lstrip())


class Any(CommandParam):
    def __init__(self, name, is_optional=False, allowed_chars="."):
        self.name = name
        self.is_optional = is_optional
        self.allowed_chars = allowed_chars
        if " " in name:
            raise Exception("One or more spaces found in command param '%s'." % name)

    def get_regex(self):
        regex = r"(\s+%s+?)" % self.allowed_chars
        return regex + ("?" if self.is_optional else "")

    def get_name(self):
        if self.is_optional:
            return "[%s]" % self.name
        else:
            return "%s" % self.name

    def process_matches(self, params):
        val = params.pop(0)
        if val is None:
            return None
        else:
            return val.lstrip()
