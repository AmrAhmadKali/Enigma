import collections
import inspect
import json
import re
import typing

from websockets.legacy.server import WebSocketServerProtocol

from meta.base_module import BaseModule
from meta.command_param_types import CommandParam
from meta.decorators import instance
from meta.dict_object import DictObject
from meta.registry import get_attrs

if typing.TYPE_CHECKING:
    from core.main import Server
    from meta.registry import Registry


@instance()
class CommandService(BaseModule):
    handlers = {}

    def __init__(self):
        self.handlers = collections.defaultdict(list)

    def inject(self, registry):
        self.bot: Server = registry.get_instance("app")
        self.reg: Registry = registry

    def start(self):
        # process decorators
        for _, inst in self.reg.get_all_instances().items():
            for name, method in get_attrs(inst).items():
                if hasattr(method, "command"):
                    key = self.reg.get_module_name(inst).split(".")
                    if key[0] not in self.bot.modules:
                        continue
                    cmd_name, params, description, sub_command = getattr(
                        method, "command")
                    handler = getattr(inst, name)
                    print(
                        f"Registering command '{cmd_name}{(' ' + sub_command) if sub_command else ''}' with parameters: '{', '.join([x.get_name() for x in params])}'")
                    self.register(handler, cmd_name, params, description, inst.module_name, sub_command)

    def register(self, handler: callable, command: str, params: typing.List[CommandParam],
                 description: str, module: str, sub_command: str = None) -> None:
        """
        This function will register a command for future use in the websocket Server.
        :param handler: callback to the function handling the command
        :param command: main command this handler will listen to
        :param params: Command Parameters for the handler
        :param description: Description of the Command (what does it do?)
        :param module: owning module of the command handler
        :param sub_command: sub command associated with the handler
        """
        if len(inspect.signature(handler).parameters) != len(params) + 2:
            raise Exception(
                f"Incorrect number of arguments for handler '{handler.__module__}.{handler.__name__}()'")

        command = command.lower()
        if sub_command:
            sub_command = sub_command.lower()
        else:
            sub_command = ""
        command_key = self.get_command_key(command, sub_command)
        r = re.compile(self.get_regex_from_params(params), re.IGNORECASE | re.DOTALL)
        self.handlers[command_key].append({'regex': r, "callback": handler, "description": description,
                                           "params": params, "module": module, 'cmd': command_key})

    async def reply(self, client: WebSocketServerProtocol, resp: object) -> None:
        """
        Using this you may send a response to the client which is currently being handled.
        :param client: Websocket connection this response should be sent to
        :param resp: Status Code, and possibly data
        :return: Nothing will be returned.
        """
        if resp:
            if type(resp) == tuple and len(resp) == 2:
                status, response = resp
                await client.send(json.dumps({'status': status, 'response': response}))
                return
            await client.send(json.dumps({'status': resp}))

    async def process_command(self, client: WebSocketServerProtocol, message: DictObject, storage: DictObject) -> None:
        """
        Here we'll run commands received from a client.
        :param client: Websocket connection of the client requesting a command to be executed
        :param message: data the client has sent us
        :param storage: Storage space associated with the currently connected client
        :return: Nothing will be returned.
        """
        params = ""
        if message.get('params', None):
            params = " " + ''.join([str(x) for x in message.get('params', [])])
        cmd = self.get_command_key(message.cmd, message.get('sub_cmd', None))
        key, matches, handler = self.get_matches(cmd, params)
        if not handler:
            await self.reply(client, 404)
            return
        # TODO: error handling! prevent the storage from getting corrupted in the first place
        resp = await handler["callback"](client, storage, *self.process_matches(matches, handler["params"]))
        storage.usages += 1
        await self.reply(client, resp)

    def get_command_key(self, command: str, sub_command: str) -> str:
        """
        Merge main command and sub command for searching in the command map
        :param command: Main command
        :param sub_command: Sub Command
        :return: Key for searching in the handler Map
        """
        if sub_command:
            return command + ":" + sub_command
        else:
            return command

    def process_matches(self, matches: re, params: typing.List[CommandParam]) -> [object]:
        """
        Convert a matched regex to parameters for the function to use
        :param matches: regex match over the command parameters
        :param params: List of Command Parameter types to parse
        :return: parameters used by the command handler, ready to use
        """
        groups = list(matches.groups())

        processed = []
        for param in params:
            processed.append(param.process_matches(groups))
        return processed

    def get_matches(self, command_key: str, command_args: str) -> object:
        """
        Find the handler matching the command key aswell as the arguments provided based on regex.
        :param command_key: Key for searching in the handler list.
        :param command_args: Arguments passed to the command handler.
        :return: command handler which matches all provided arguments, based on the handler list. None if no match
        """
        handlers = self.handlers[command_key]
        for handler in handlers:
            # add leading space to search string to normalize input for command params
            matches = handler["regex"].search(command_args)
            if matches:
                return command_key, matches, handler
        return None, None, None

    def get_regex_from_params(self, params: typing.List[CommandParam]):
        """
        Convert CommandParam types to an easy-to-use regex string
        :param params: list of Command Parameters this command expects.
        :return: regex expression used for validating command usages.
        """

        # params must be wrapped with line-beginning and line-ending anchors in order to match
        # when no params are specified (eg. "^$")
        return "^" + "".join(map(lambda x: x.get_regex(), params)) + "$"
