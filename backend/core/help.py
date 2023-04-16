from meta.base_module import BaseModule
from meta.decorators import instance, command
from meta.dict_object import DictObject


@instance("help")
class Addon2(BaseModule):

    def inject(self, reg):
        self.app = reg.get_instance("app")
        self.command_service = reg.get_instance("command_service")

    @command(command="help", params=[],
             description="This command will return an index of all available commands.")
    async def handler1(self, _, _1):
        data = []
        for key, val in self.command_service.handlers.items():
            for handler in val:
                handler = DictObject(handler)
                l = {"cmd": key, "params": ', '.join([x.get_name() for x in handler.params]),
                     "desc": handler.description}
                data.append(l)
        return 200, data
