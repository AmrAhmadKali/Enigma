Feature: Option Menu

  Scenario Outline: Test Enigma variants with the different Rotors and Reflectors
   Given The Enigma Website is opened
    When I click setting symbol
    And I choose the variant <variant>
    And I choose the Reflector <reflector>
    And I choose the Rotor 1 <rotor1>
    And I choose the Rotor 2 <rotor2>
    And I choose the Rotor 3 <rotor3>
    And I click submit
    And I press the G key on the physical keyboard
    Then The letter <encrypted_letter> should be displayed in the output box

    Examples:
    | variant | reflector   | rotor1      | rotor2      | rotor3      | encrypted_letter |
    | 1       | Reflector A | Enigma I-R1 | Enigma I-R2 | Enigma I-R3 | U                |
    | 1       | Reflector A | Enigma I-R1 | Enigma I-R4 | Enigma I-R5 | U                |

    | 1       | Reflector B | Enigma I-R1 | Enigma I-R2 | Enigma I-R3 | X                |
    | 1       | Reflector B | Enigma I-R1 | Enigma I-R4 | Enigma I-R5 | O                |

    | 1       | Reflector C | Enigma I-R1 | Enigma I-R2 | Enigma I-R3 | J                |
    | 1       | Reflector C | Enigma I-R1 | Enigma I-R4 | Enigma I-R5 | J                |

    | M3      | Reflector B | Enigma M3-R1 | Enigma M3-R2 | Enigma M3-R3 | X             |
    | M3      | Reflector B | Enigma M3-R4 | Enigma M3-R1 | Enigma M3-R5 | O             |

    | M3      | Reflector C | Enigma M3-R6 | Enigma M3-R7 | Enigma M3-R8 | D             |

   # ToDo Test Cases for Enigma B variant when it is ready
