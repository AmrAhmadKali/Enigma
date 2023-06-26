Feature: Option Menu

  Scenario Outline: Test Enigma standard variants with the different Rotors and Reflectors
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
    | Enigma 1       | Reflector A | Enigma I-R1 | Enigma I-R2 | Enigma I-R3 | U                |
    | Enigma 1       | Reflector A | Enigma I-R1 | Enigma I-R4 | Enigma I-R5 | U                |

    | Enigma 1       | Reflector B | Enigma I-R1 | Enigma I-R2 | Enigma I-R3 | X                |
    | Enigma 1       | Reflector B | Enigma I-R1 | Enigma I-R4 | Enigma I-R5 | O                |

    | Enigma 1       | Reflector C | Enigma I-R1 | Enigma I-R2 | Enigma I-R3 | J                |
    | Enigma 1       | Reflector C | Enigma I-R1 | Enigma I-R4 | Enigma I-R5 | J                |

    | Enigma B       | Reflector UKW | Enigma B-R1 | Enigma B-R2 | Enigma B-R3 | S                |

    | Enigma M3      | Reflector B | Enigma M3-R1 | Enigma M3-R2 | Enigma M3-R3 | X             |
    | Enigma M3      | Reflector B | Enigma M3-R4 | Enigma M3-R1 | Enigma M3-R5 | O             |

    | Enigma M3      | Reflector C | Enigma M3-R6 | Enigma M3-R7 | Enigma M3-R8 | D             |


  Scenario Outline: Plugboard disabled for Variant B
    Given The Enigma Website is opened
    When I click setting symbol
    And I choose the variant <variant>
    And I choose the Reflector <reflector>
    And I choose the Rotor 1 <rotor1>
    And I choose the Rotor 2 <rotor2>
    And I choose the Rotor 3 <rotor3>
    And I click submit
    And I press the G key on the physical keyboard
    Then Plugboard is disappeared
    And The letter <encrypted_letter> should be displayed in the output box


    Examples:
      | variant |  reflector    | rotor1      | rotor2      | rotor3      | encrypted_letter |
      | Enigma B  |  Reflector UKW   | Enigma B-R3  |  Enigma B-R2  |  Enigma B-R1   |     S    |


    Scenario Outline: Set Rotor offset
      Given The Enigma Website is opened
      When I click setting symbol
      And I choose the variant <variant>
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
      | variant |  reflector    | rotor1      | rotor2      |    rotor3     |        offset1         |      offset2       |      offset3       | encrypted_letter |
      |  Enigma M3  |  Reflector C   |  Enigma M3-R8  |  Enigma M3-R7  |   Enigma M3-R6  |        B         |         D         |           Z         |         Q        |


      Scenario Outline: Set Ring settings
        Given The Enigma Website is opened
        When I click setting symbol
        And I choose the variant <variant>
        And I choose the Reflector <reflector>
        And I choose the Rotor 1 <rotor1>
        And I choose the Rotor 2 <rotor2>
        And I choose the Rotor 3 <rotor3>
        And I set rotor 1 offset to <offset1>
        And I set rotor 2 offset to <offset2>
        And I set rotor 3 offset to <offset3>
        And I set rotor 1 ring setting to <ring1>
        And I set rotor 2 ring setting to <ring2>
        And I set rotor 3 ring setting to <ring3>
        And I click submit
        And I press the G key on the physical keyboard
        Then The letter <encrypted_letter> should be displayed in the output box


        Examples:
          | variant |  reflector | rotor1 | rotor2  |  rotor3  |   offset1    |   offset2   |   offset3    |  ring1 | ring2 | ring3 | encrypted_letter  |
          | Enigma 1 |  Reflector A | Enigma I-R3 | Enigma I-R4  |  Enigma I-R5  |   A    |   A   |   A    |  2     | 5     | 7     |        H          |
          | Enigma 1 |  Reflector A | Enigma I-R3 | Enigma I-R4  |  Enigma I-R5  |   B    |   D   |   F    |  2     | 5     | 7     |        V          |
