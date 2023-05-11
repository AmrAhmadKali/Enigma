import typing

from websockets.legacy.server import WebSocketServerProtocol

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
    async def help_cmd(self, _: WebSocketServerProtocol, _1: DictObject) -> typing.Tuple[int, typing.Any]:
        """
        Return a list of all commands, with their parameters and description to the client
        :param _: Websocket connection executing this command
        :param _1: storagespace used by this command
        :return:
        """
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
    async def dump_cmd(self, _: WebSocketServerProtocol, storage: DictObject) -> typing.Tuple[int, typing.Any]:
        """
        Return the whole storage space to the client
        :param _: Websocket connection executing this command
        :param storage: storagespace used by this command
        :return:
        """
        return 200, storage
