import typing
from typing import Tuple

from websockets.legacy.server import WebSocketServerProtocol

from meta.base_module import BaseModule
from meta.command_param_types import Reflector, Multiple, Rotor, Int, Any
from meta.decorators import instance, command
from meta.dict_object import DictObject

if typing.TYPE_CHECKING:
    from core.rotor_service import RotorService


@instance()
class RotorController(BaseModule):
    def inject(self, reg) -> None:
        self.rotor_service: RotorService = reg.get_instance('rotor_service')

    @command(command="rotors",
             params=[],
             description="Shows a list of all available Rotors.")
    async def rotors_help_cmd(self, _: WebSocketServerProtocol, _1: DictObject) -> Tuple[int, str]:
        return 200, [x for x in self.rotor_service.rotors.keys() if 'Reflector' not in x]

    @command(command="rotors",
             sub_command='set',
             params=[Reflector('Reflector'), Multiple(Rotor('Rotors'), 3, 3)],
             description="Change the full Rotor/Reflector Setup, from left to right.")
    async def rotors_set_all_cmd(self, _: WebSocketServerProtocol, storage: DictObject, reflector: str,
                                 rotors: list[str]) -> Tuple[int, str]:
        for rotor in rotors:
            if rotor not in self.rotor_service.rotors:
                return 400, f"The Rotor '{rotor}' does not exist"
        if reflector not in self.rotor_service.rotors:
            return 400, f"The Reflector '{reflector}' does not exist"

        storage.rotor_order = [[x for x in reversed(rotors)], reflector]
        self.rotor_service.reset_offsets(storage)
        return 200, "Preset Changed"

    @command(command="reflector",
             sub_command='set',
             params=[Reflector('Reflector', is_optional=True)],
             description="Change the used Reflector. Will display index of Reflectors if UNDEF")
    async def reflector_set_cmd(self, _: WebSocketServerProtocol,
                                storage: DictObject,
                                reflector: str) \
            -> Tuple[int, str]:
        if not reflector:
            return 200, [x for x in self.rotor_service.rotors.keys() if 'Reflector' in x]
        if reflector not in self.rotor_service.rotors:
            return 400, f"The Reflector '{reflector}' does not exist"

        storage.rotor_order[1] = reflector
        self.rotor_service.reset_offsets(storage)
        return 200, "Preset Changed"

    @command(command="rotors",
             sub_command='set',
             params=[Int('rotor_id'), Rotor('Rotor')],
             description="Swap a rotor. ID 0 comes after reflector, 1 middle, 2 right")
    async def rotors_set_single_cmd(self, _: WebSocketServerProtocol,
                                    storage: DictObject,
                                    rotor_id: int,
                                    rotor: str) -> \
            Tuple[int, str]:
        if rotor_id < 0 or \
                2 < rotor_id:
            return 400, 'ID mismatch'
        if rotor not in self.rotor_service.rotors:
            return 400, f"The Reflector '{rotor}' does not exist"

        storage.rotor_order[0][rotor_id] = rotor
        self.rotor_service.reset_offsets(storage)
        return 200, "Preset Changed"

    @command(command="rotors",
             sub_command='offset',
             params=[Int('rotor_id'), Any('offset', allowed_chars='[a-zA-Z]')],
             description="Set the Offset of a single Rotor. ID 0 comes after reflector, 1 middle, 2 right. Example param: 'ABC'")
    async def rotors_offset_single_cmd(self, _: WebSocketServerProtocol,
                                       storage: DictObject,
                                       rotor_id: int,
                                       offset: str) -> \
            Tuple[int, str]:
        if rotor_id > len(storage.rotor_order):
            return 400, 'Out of Bounds'
        if len(offset) != 1:
            return 400, 'please provide an offset with the length 1'

        storage.rotors[storage.rotor_order[0][rotor_id]] = self.rotor_service.convert_to_int(offset)[0]
        return 200, "Offset Adjusted."

    @command(command="rotors",
             sub_command='offset',
             params=[Any('offset', allowed_chars='[a-zA-Z]')],
             description="Set the Offset of all Rotors. ID 0 comes after reflector, 1 middle, 2 right. Example param: 'ABC'")
    async def rotors_offset_all_cmd(self, _: WebSocketServerProtocol,
                                    storage: DictObject,
                                    offset: [str]) -> \
            Tuple[int, str]:
        if len(offset) != 3:
            return 400, 'Please provide an offset with the length 3'
        for i, rotor in enumerate(storage.rotor_order[0]):
            storage.rotors[rotor] = self.rotor_service.convert_to_int(offset[i])[0]
        return 200, "Offset Adjusted."
