Feature: Option Menu

#
#  Scenario Outline: Test Enigma variants with the different Rotors and Reflectors
#   Given The Enigma Website is opened
#    When I click setting symbol
#    And I choose the variant <variant>
#    And I choose the Reflector <reflector>
#    And I choose the Rotor 1 <rotor1>
#    And I choose the Rotor 2 <rotor2>
#    And I choose the Rotor 3 <rotor3>
#    And I click submit
#    And I press the G key on the physical keyboard
#    Then The letter <encrypted_letter> should be displayed in the output box
#
#    Examples:
#    | variant | reflector   | rotor1      | rotor2      | rotor3      | encrypted_letter |
#    | 1       | Reflector A | Enigma I-R1 | Enigma I-R2 | Enigma I-R3 | U                |
#    | 1       | Reflector A | Enigma I-R1 | Enigma I-R4 | Enigma I-R5 | U                |
#
#    | 1       | Reflector B | Enigma I-R1 | Enigma I-R2 | Enigma I-R3 | X                |
#    | 1       | Reflector B | Enigma I-R1 | Enigma I-R4 | Enigma I-R5 | O                |
#
#    | 1       | Reflector C | Enigma I-R1 | Enigma I-R2 | Enigma I-R3 | J                |
#    | 1       | Reflector C | Enigma I-R1 | Enigma I-R4 | Enigma I-R5 | J                |
#
#    | M3      | Reflector B | Enigma M3-R1 | Enigma M3-R2 | Enigma M3-R3 | X             |
#    | M3      | Reflector B | Enigma M3-R4 | Enigma M3-R1 | Enigma M3-R5 | O             |
#
#    | M3      | Reflector C | Enigma M3-R6 | Enigma M3-R7 | Enigma M3-R8 | D             |
#
#   # ToDo Test Cases for Enigma B variant when it is ready



  Scenario Outline: Plugboard Existence when not checked in settings
    Given The Enigma Website is opened
    When I click setting symbol
    # Dont have to select default for Variant because it 's by default selected
    And I choose the Reflector <reflector>
    And I choose the Rotor 1 <rotor1>
    And I choose the Rotor 2 <rotor2>
    And I choose the Rotor 3 <rotor3>
    And I uncheck the Plugboard checkbox
    And I click submit
    And I press the G key on the physical keyboard
    Then Plugboard is disappeared
    And The letter <encrypted_letter> should be displayed in the output box


    Examples:
      |  reflector    | rotor1      | rotor2      | rotor3      | encrypted_letter |
      |  Reflector B   | Enigma I-R2  |  Enigma B-R2  |  Enigma M3-R3   |     Y    |


    Scenario Outline: Rotor offsetsss
      Given The Enigma Website is opened
      When I click setting symbol
    # Dont have to select default for Variant because it 's by default selected
      And I choose the Reflector <reflector>
      And I choose the Rotor 1 <rotor1>
      And I choose the Rotor 2 <rotor2>
      And I choose the Rotor 3 <rotor3>
      And I set rotor 1 offset to <offset1>
      And I set rotor 2 offset to <offset2>
      And I set rotor 3 offset to <offset3>
      And I click submit
      And I press the G key on the physical keyboard
      Then The letter <encrypted_letter> should be displayed in the output box


      Examples:
      |  reflector    | rotor1      | rotor2      |    rotor3     |        offset1         |      offset2       |      offset3       | encrypted_letter |
      |  Reflector C   |  Enigma I-R5  |  Enigma B-R3  |   Enigma M3-R8  |        B         |         D         |           Z         |         U        |
