# Enigma B, I and M3
from abc import ABC


#   THESE CLASSES
#   ARE NOT IN THE
#   REGISTRY!

# META

# Blank Rotor
class Rotor:
    mapping = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Default mapping


# Enigma I
class EIRotor1(Rotor):
    mapping = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    notch = "Q"


class EIRotor2(Rotor):
    mapping = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    notch = "E"


class EIRotor3(Rotor):
    mapping = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    notch = "V"


# Enigma B
class EBRotor1(Rotor):
    mapping = "DMTWSILRUYQNKFEJCAZBPGXOHV"
    notch = "Q"


class EBRotor2(Rotor):
    mapping = "HQZGPJTMOBLNCIFDYAWVEUSRKX"
    notch = "E"


class EBRotor3(Rotor):
    mapping = "UQNTLSZFMREHDPXKIBVYGJCWOA"
    notch = "V"


# Enigma M3
class M3Rotor4(Rotor):
    mapping = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    notch = "J"


class M3Rotor5(Rotor):
    mapping = "VZBRGITYUPSDNHLXAWMJQOFECK"
    notch = "Z"


class ReflectorA(Rotor):
    mapping = "EJMZALYXVBWFCRQUONTSPIKHGD"


class ReflectorB(Rotor):
    mapping = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


class ReflectorC(Rotor):
    mapping = "FVPJIAOYEDRZXWGCTKUQSBNMHL"
