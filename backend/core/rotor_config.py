import random

from meta.base_module import BaseModule
from meta.decorators import instance


@instance()
class Rotors(BaseModule):
    rotors = {  # name: [mapping, notch]
        'Reflector A': ["EJMZALYXVBWFCRQUONTSPIKHGD"],
        'Reflector B': ["YRUHQSLDPXNGOKMIEBFZCWVJAT"],
        'Reflector C': ["FVPJIAOYEDRZXWGCTKUQSBNMHL"],
        # 'Enigma I-R2': ["AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"],
        # 'Enigma I-R3': ["BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"],
    }

    async def setup(self, storage):
        # Pick a random Reflector...
        # TODO: replace with real rotor/reflector logic.
        storage.rotors = self.rotors.get(random.choice([x for x in self.rotors.keys()]))[0]

    def encrypt(self, storage, key):
        return storage.rotors[int(key, 36) - 10]
