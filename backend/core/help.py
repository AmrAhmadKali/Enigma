import typing

from meta.base_module import BaseModule
from meta.decorators import instance, command
from meta.dict_object import DictObject

if typing.TYPE_CHECKING:
    from core.main import Server
    from core.command_service import CommandService


@instance("help")
class Addon2(BaseModule):

    def inject(self, reg):
        self.app: Server = reg.get_instance("app")
        self.command_service: CommandService = reg.get_instance("command_service")

    @command(command="help", params=[],
             description="This command will return an index of all available commands.")
    async def help_cmd(self, _, _1):
        data = []
        for key, val in self.command_service.handlers.items():
            for handler in val:
                handler = DictObject(handler)
                entry = {"cmd": key, "params": ', '.join([x.get_name() for x in handler.params]),
                         "desc": handler.description}
                data.append(entry)
        return 200, data

    # TODO: remove in RELEASE build. DEBUGGING PURPOSES ONLY!
    # Possibly: add a FEATURE_FLAG, which enables/disables including this command.
    @command(command="dump", params=[],
             description="this will dump the whole storage to the client")
    async def dump_cmd(self, _, storage):
        return 200, storage
