from meta.base_module import BaseModule
from meta.command_param_types import Any
from meta.decorators import instance, command


@instance()
class Plugboard(BaseModule):

    async def setup(self, storage):

        storage.plugboard = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @command(command="plugboard", sub_command="set", params=[Any("setting")],
    description="Set the Plugboard Configuration")
    async def pb_set_cmd(self, ws, storage, pbs):
        if(len(pbs) % 2 == 1):
            return 400, "Uneven variable count"
        if(len(pbs) != 2):
            return 300, "Variable count not 2"
        if not (pbs.isalpha()):
            return 400, "Received non alphabetical letters"
        pbs = pbs.upper()
        x = storage.plugboard.find(pbs[0])
        y = storage.plugboard.find(pbs[1])
        storage.plugboard[x] = pbs[1]
        storage.plugboard[y] = pbs[0]
        return 200

    @command(command="plugboard", sub_command="reset", params=[],
    description="Reset the Plugboard Configuration to default")
    async def pb_reset_cmd(self, ws, storage):
        storage.plugboard = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return 200

    def encrypt(self, storage, key):
        return storage.plugboard["ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(key)]
