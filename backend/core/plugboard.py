from meta.base_module import BaseModule
from meta.command_param_types import Any
from meta.decorators import instance, command


@instance()
class Plugboard(BaseModule):

    async def setup(self, storage):

        storage.plugboard = {}

    @command(command="plugboard", sub_command="set", params=[Any("setting")],
             description="Set the Plugboard Configuration")
    async def pb_set_cmd(self, _, storage, pbs):
        if len(pbs) % 2 == 1:
            return 400, "Uneven variable count"
        if len(pbs) != 2:
            return 300, "Variable count not 2"
        if not (pbs.isalpha()):
            return 400, "Received non alphabetical letters"
        pbs = pbs.upper()
        a, b = pbs
        if a in storage.plugboard and b in storage.plugboard:
            storage.plugboard.pop(a)
            storage.plugboard.pop(b)
            return 200
        if a in storage.plugboard:
            return 300, f"There's already a mapping for {a}"
        if b in storage.plugboard:
            return 300, f"There's already a mapping for {b}"

        storage.plugboard[a] = b
        storage.plugboard[b] = a
        return 200

    @command(command="plugboard", sub_command="reset", params=[],
             description="Reset the Plugboard Configuration to default")
    async def pb_reset_cmd(self, _, storage):
        storage.plugboard = {}
        return 200

    def encrypt(self, storage, key):
        return storage.plugboard.get(key, key)
