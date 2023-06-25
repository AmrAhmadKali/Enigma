Feature: Session

  Scenario Outline: Delete settings to recover default settings
    Given The Enigma Website is opened
    When I click setting symbol
    And I choose the variant <variant>
    And I choose the Reflector <reflector>
    And I choose the Rotor 1 <rotor1>
    And I choose the Rotor 2 <rotor2>
    And I choose the Rotor 3 <rotor3>
    And I click submit
    And I press the reset button
    And I close the Alert
    And I click setting symbol
    Then Variant is set to <default_variant>
    And Reflector is set to <default_reflector>
    And Rotor 1 is set to <default_rotor1>
    And Rotor 2 is set to <default_rotor2>
    And Rotor 3 is set to <default_rotor3>


    Examples:
      | variant | reflector   | rotor1      | rotor2      | rotor3      | default_variant  |  default_reflector | default_rotor1 |  default_rotor2  | default_rotor3  |
      | Enigma M3 | Reflector C   | Enigma M3-R8      | Enigma M3-R7      | Enigma M3-R6      | Enigma 1  | Reflector A | Enigma I-R1 | Enigma I-R2 | Enigma I-R3 |


    Scenario: test cookies, save state
      Given The Enigma Website is opened
      When I click setting symbol
      And I choose the variant Enigma B
      And I choose the Reflector Reflector UKW
      And I choose the Rotor 1 Enigma B-R3
      And I choose the Rotor 2 Enigma B-R2
      And I choose the Rotor 3 Enigma B-R1
      And I click submit
      When I refresh page and close Alert
      And I click setting symbol
      Then Variant is set to Enigma B
      And Reflector is set to UKW Enigma B
      And Rotor 1 is set to Enigma B-R3
      And Rotor 2 is set to Enigma B-R2
      And Rotor 3 is set to Enigma B-R1