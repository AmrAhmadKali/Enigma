from meta.base_module import BaseModule
from meta.decorators import instance
from meta.dict_object import DictObject


@instance()
class RotorService(BaseModule):

    def start(self):
        self.basemap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.rotors = {  # name: [mapping, turnover, notch]
            # Reflectors
            'Reflector A': ["EJMZALYXVBWFCRQUONTSPIKHGD"],
            'Reflector B': ["YRUHQSLDPXNGOKMIEBFZCWVJAT"],
            'Reflector C': ["FVPJIAOYEDRZXWGCTKUQSBNMHL"],
            # Enigma I
            'Enigma I-R1': ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", self.convert_to_int("Q"), self.convert_to_int("Y")],
            'Enigma I-R2': ["AJDKSIRUXBLHWTMCQGZNPYFVOE", self.convert_to_int("E"), self.convert_to_int("M")],
            'Enigma I-R3': ["BDFHJLCPRTXVZNYEIWGAKMUSQO", self.convert_to_int("V"), self.convert_to_int("D")],
            'Enigma I-R4': ["ESOVPZJAYQUIRHXLNFTGKDCMWB", self.convert_to_int("J"), self.convert_to_int("R")],
            'Enigma I-R5': ["VZBRGITYUPSDNHLXAWMJQOFECK", self.convert_to_int("Z"), self.convert_to_int("H")],
            # Enigma B
            'Enigma B-R1': ["DMTWSILRUYQNKFEJCAZBPGXOHV", self.convert_to_int("Q"), self.convert_to_int("")],
            'Enigma B-R2': ["HQZGPJTMOBLNCIFDYAWVEUSRKX", self.convert_to_int("E"), self.convert_to_int("")],
            'Enigma B-R3': ["UQNTLSZFMREHDPLKIBVYGJCWOA", self.convert_to_int("V"), self.convert_to_int("")],
            # Enigma M3
            'Enigma M3-R1': ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", self.convert_to_int("Q"), self.convert_to_int("Y")],
            'Enigma M3-R2': ["AJDKSIRUXBLHWTMCQGZNPYFVOE", self.convert_to_int("E"), self.convert_to_int("M")],
            'Enigma M3-R3': ["BDFHJLCPRTXVZNYEIWGAKMUSQO", self.convert_to_int("V"), self.convert_to_int("D")],
            'Enigma M3-R4': ["ESOVPZJAYQUIRHXLNFTGKDCMWB", self.convert_to_int("J"), self.convert_to_int("R")],
            'Enigma M3-R5': ["VZBRGITYUPSDNHLXAWMJQOFECK", self.convert_to_int("Z"), self.convert_to_int("H")],
            'Enigma M3-R6': ["JPGVOUMFYQBENHZRDKASXLICTW", self.convert_to_int("ZM"), self.convert_to_int("HU")],
            'Enigma M3-R7': ["NZJHGRCXMYSWBOUFAIVLPEKQDT", self.convert_to_int("ZM"), self.convert_to_int("HU")],
            'Enigma M3-R8': ["FKQHTLXOCBJSPDZRAMEWNIUYGV", self.convert_to_int("ZM"), self.convert_to_int("HU")],

        }

    async def setup(self, storage: DictObject) -> None:
        # Setting up of the Rotor Chain
        # By Default, we'll use:
        #  - Enigma I - A-I-II-III
        #  - KEY (rotor offset) AAA

        storage.rotor_order = [
            ['Enigma I-R3', 'Enigma I-R2', 'Enigma I-R1'],
            'Reflector A',  # Forward
        ]
        self.reset_offsets(storage)

    def reset_offsets(self, storage):
        storage.rotors = {}
        for x in storage.rotor_order[0]:
            storage.rotors[x] = 0

    def _rotate(self, storage: DictObject, rotor: str, n: int = 1) -> None:
        """
        Rotate a specific rotor 'rotor' in 'storage' by 'n' letters forwards.
        :param storage: Storage space in which we can find the current rotor.
        :param rotor: rotor which should be rotated.
        :param n: number of letters it should be rotated.
        """
        storage.rotors[rotor] += n

    def _perform_rotate(self, storage: DictObject) -> None:
        """
        perform natural rotor rotation
        :param storage: Storage space in which we can find the used rotors & offsets
        """

        r1 = storage.rotor_order[0][2]
        r2 = storage.rotor_order[0][1]
        r3 = storage.rotor_order[0][0]

        # notch might be a list!
        if (storage.rotors[r2] % 26) in self.rotors[r2][1] \
                and (storage.rotors[r3] % 26) in self.rotors[r3][1]:
            self._rotate(storage, r1)
            self._rotate(storage, r2)
            self._rotate(storage, r3)
        elif (storage.rotors[r2] % 26) in self.rotors[r2][1]:
            self._rotate(storage, r1)
            self._rotate(storage, r2)
            self._rotate(storage, r3)
        elif (storage.rotors[r3] % 26) in self.rotors[r3][1]:
            self._rotate(storage, r2)
            self._rotate(storage, r3)
        else:
            self._rotate(storage, r3)

    def encrypt(self, storage: DictObject, key: str) -> str:
        """
        Encrypt a letter based on the parameters outlines in 'storage'.
        :param storage: Storage space allocated to the current client, containing parameters for encryption.
        :param key: the letter which should be encrypted.
        :return: encrypted letter.
        """
        self._perform_rotate(storage)
        key = self.convert_to_int(key)[0]
        for x in storage.rotor_order[0]:
            key = self.forward(x, key, storage.rotors[x])
        key = self.forward(storage.rotor_order[1], key, 0)

        for x in reversed(storage.rotor_order[0]):
            key = self.backward(x, key, storage.rotors[x])
        return self.convert_to_str(key)

    def forward(self, rotor: str, signal: int, offset: int) -> int:
        """
        Forward encryption of a rotor;
        If rotor is a deflector, offset == 0
        :param rotor: Rotor through which we are passing right now
        :param signal: current int value (for simulating a specific wire) of the input
        :param offset: Offset of the current rotor.
        :return:
        """
        letter = self.rotors[rotor][0][(signal + offset) % 26]
        signal = self.basemap.find(letter) - (offset % 26)
        return signal

    def backward(self, rotor: str, signal: int, offset: int) -> int:
        """
         Backwards encryption of a rotor;
         :param rotor: Rotor through which we are passing right now
         :param signal: current int value (for simulating a specific wire) of the input
         :param offset: Offset of the current rotor.
         :return:
         """
        letter = self.basemap[(signal + offset) % 26]
        signal = self.rotors[rotor][0].find(letter) - (offset % 26)
        return signal

    def convert_to_int(self, keys: str) -> [int]:
        """
        Convert Keys to a list of ints, for rotor usage.
        :param keys: Keys to convert
        :return: List of int values of the key
        """
        return ["ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(key) for key in keys]

    def convert_to_str(self, key: int) -> str:
        """
        Convert signal/int to letter.
        :param key: Int value of a letter.
        :return: Letter.
        """
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[key]
