# DO NOT TOUCH UNLESS YOU'RE 100% SURE WHAT YOU'RE DOING!
import abc
import re
from typing import List, Union


class CommandParam(abc.ABC):
    is_optional = False

    def get_regex(self) -> str:
        """
        Get the Regex used by this command parameter.
        :return:
        """

    def get_name(self) -> str:
        """
        Get the Name of the Parameter.
        :return:
        """

    def process_matches(self, params: List[str]) -> Union[None, str]:
        """

        :param params: List of remaining parameters
        :return: Parameter matching this Type
        """


class Const(CommandParam):
    """
    This is a Constant Parameter type for usage by Command Handlers.
    It will only match, if the name is exactly matched.
    """

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
    """
    This is an Int Parameter type for usage by Command Handlers.
    It will only match, if a decimal number is being provided.
    """

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


class Hex(CommandParam):
    """
    This is a Hex Parameter type for usage by Command Handlers.
    It will only match, if a decimal number is being provided.
    """

    def __init__(self, name, is_optional=False):
        self.name = name
        self.is_optional = is_optional
        if " " in name:
            raise Exception("One or more spaces found in command param '%s'." % name)

    def get_regex(self):
        regex = r"(\s+(0x)?[0-9a-fA-F]+)"
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
            return int(val.lstrip(), 16)


class Any(CommandParam):
    """
    This is a "catchall" Parameter type for usage by Command Handlers.
    By default, it will match any number, character or symbol.
    """

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


class Rotor(CommandParam):
    """
    This is a "catchall" Parameter type for usage by Command Handlers.
    By default, it will match any number, character or symbol.
    """

    def __init__(self, name, is_optional=False):
        self.name = name
        self.is_optional = is_optional
        if " " in name:
            raise Exception("One or more spaces found in command param '%s'." % name)

    def get_regex(self):
        regex = r"(\s+Enigma .+?-R[1-8])"
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


class Reflector(CommandParam):
    """
    This is a "catchall" Parameter type for usage by Command Handlers.
    By default, it will match any number, character or symbol.
    """

    def __init__(self, name, is_optional=False, allowed_chars="."):
        self.name = name
        self.is_optional = is_optional
        self.allowed_chars = allowed_chars
        if " " in name:
            raise Exception("One or more spaces found in command param '%s'." % name)

    def get_regex(self):
        regex = r"(\s+Reflector [A-Z]+?)"
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


class Multiple(CommandParam):
    def __init__(self, inner_type, min_num=1, max_num=None):
        if type(inner_type) is Any:
            # Any type ignores is_optional and allowed_chars params, and can only capture
            # single words (no spaces) when used with Multiple
            def get_regex():
                regex = r"(\s+[^ ]+)"
                return regex

            inner_type.get_regex = get_regex

        self.inner_type = inner_type
        self.min = min_num or ""
        self.max = max_num or ""

    def get_regex(self):
        regex = "(" + self.inner_type.get_regex() + "{%s,%s})" % (self.min, self.max)
        return regex

    def get_name(self):
        return self.inner_type.get_name() + "*"

    def process_matches(self, params):
        v = params.pop(0)

        # remove unused params
        self.inner_type.process_matches(params)

        results = []
        p = re.compile(self.inner_type.get_regex(), re.IGNORECASE | re.DOTALL)

        matches = p.search(v)
        while matches:
            v = v[matches.end():]
            a = self.inner_type.process_matches(list(matches.groups()))
            results.append(a)
            matches = p.search(v)

        return results
