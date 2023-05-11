# DO NOT TOUCH UNLESS YOU'RE 100% SURE WHAT YOU'RE DOING!
import abc
from typing import List


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

    def process_matches(self, params: List[str]) -> None | str:
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
