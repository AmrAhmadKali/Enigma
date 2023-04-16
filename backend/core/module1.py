from core import main
from meta.base_module import BaseModule
from meta.command_param_types import Int
from meta.decorators import instance, command


@instance("addon1")
class Addon(BaseModule):
    app: main.Server

    def inject(self, reg):
        self.app = reg.get_instance("app")

    @command(command="set", sub_command="rotor", params=[Int('rotor_id'), Int('counter', is_optional=True)],
             description="This command is used for changing the counter of a specific Rotor during runtime.")
    async def handler1(self, _, _1, rotor_id, counter):
        if not counter:
            counter = 50
        return 501, f"R{rotor_id} SET C{counter}"

    @command(command="set", sub_command="rotor", params=[Int('rotor_id')],
             description="Lookup the current data about a rotor")
    async def handler2(self, _, _1, rotor_id):
        return 501, f"R{rotor_id} READ C24"
