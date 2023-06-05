from typing import List

from meta.command_param_types import CommandParam
from meta.registry import Registry


# DO NOT TOUCH UNLESS YOU'RE 100% SURE WHAT YOU'RE DOING!


# taken from: https://stackoverflow.com/a/26151604/280574

def parameterized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parameterized
def instance(cls, name=None, override=False) -> callable:
    """
    Used for registering new Modules.
    :param cls: Instance of a module
    :param name: Custom name of the Module
    :param override: if existing module with same name should be overriden
    :return:
    """
    instance_name = name if name else cls.__name__
    Registry.add_instance(instance_name, cls(), override)
    return cls


@parameterized
def command(handler: callable, command: str, params: List[CommandParam], description: str,
            sub_command: str = None) -> callable:
    """
    Used for registering new commands on the backend.
    :param handler: Command Handler this annotation belongs to
    :param command: Main Command-String used by the command
    :param params: Parameters this command utilizes
    :param description: Description of the command
    :param sub_command: Sub Command used by the command handler.
    :return:
    :return:
    """
    handler.command = [command, params, description, sub_command]
    return handler
