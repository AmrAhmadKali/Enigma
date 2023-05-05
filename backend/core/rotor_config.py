from meta.base_module import BaseModule
from meta.decorators import instance


@instance()
class Rotors(BaseModule):

    def start(self):
        self.basemap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.rotors = {  # name: [mapping, notch]
            'Reflector A': ["EJMZALYXVBWFCRQUONTSPIKHGD"],
            'Reflector B': ["YRUHQSLDPXNGOKMIEBFZCWVJAT"],
            'Reflector C': ["FVPJIAOYEDRZXWGCTKUQSBNMHL"],
            'Enigma I-R1': ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", self.convert_to_int("Q")],
            'Enigma I-R2': ["AJDKSIRUXBLHWTMCQGZNPYFVOE", self.convert_to_int("E")],
            'Enigma I-R3': ["BDFHJLCPRTXVZNYEIWGAKMUSQO", self.convert_to_int("V")],
        }

    async def setup(self, storage):
        # Setting up of the Rotor Chain
        # By Default, we'll use:
        #  - Enigma I - A-I-II-III
        #  - KEY (rotor offset) AAA

        storage.rotor_order = [
            ['Enigma I-R3', 'Enigma I-R2', 'Enigma I-R1', 'Reflector A'],  # Forward
            ['Enigma I-R1', 'Enigma I-R2', 'Enigma I-R3']  # Backwards
        ]
        storage.rotors = {}
        for x in storage.rotor_order[0]:
            # TODO: fix this: This will add an unused offset for Reflector A, but that's getting ignored
            storage.rotors[x] = 0

    def rotate_rotors(self, storage, offset=[1, 0, 0]):
        pass

    def _rotate(self, storage, rotor, n=1):
        storage.rotors[rotor] += n

    def _perform_rotate(self, storage):
        # storage.rotors = {}
        r1 = storage.rotor_order[0][2]
        r2 = storage.rotor_order[0][1]
        r3 = storage.rotor_order[0][0]
        if (storage.rotors[r2] % 26) == self.rotors[r2][1] and (storage.rotors[r3] % 26) == self.rotors[r3][1]:
            self._rotate(storage, r1)
            self._rotate(storage, r2)
            self._rotate(storage, r3)
        elif (storage.rotors[r2] % 26) == self.rotors[r2][1]:
            self._rotate(storage, r1)
            self._rotate(storage, r2)
            self._rotate(storage, r3)
        elif (storage.rotors[r3] % 26) == self.rotors[r3][1]:
            self._rotate(storage, r2)
            self._rotate(storage, r3)
        else:
            self._rotate(storage, r3)
        print("Rotated!", storage.rotors)

    def encrypt(self, storage, key):
        self._perform_rotate(storage)
        key = self.convert_to_int(key)
        for x in storage.rotor_order[0]:
            key = self.forward(x, key, storage.rotors[x])
            # key = self.forward(storage.rotors[x], key)
        for x in storage.rotor_order[1]:
            key = self.backward(x, key, storage.rotors[x])
        return self.convert_to_str(key)

    def forward(self, rotor, signal, offset):
        letter = self.rotors[rotor][0][(signal + offset) % 26]
        signal = self.basemap.find(letter) - (offset % 26)
        return signal

    def backward(self, rotor, signal, offset):
        letter = self.basemap[(signal + offset) % 26]
        signal = self.rotors[rotor][0].find(letter) - (offset % 26)
        return signal

    def convert_to_int(self, key):
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(key)

    def convert_to_str(self, key):
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[key]
