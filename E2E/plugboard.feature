Feature: Plugboard

  Scenario: Plugboard Set
    Given The Enigma Website is opened
    When I press the U key on the plugboard
    And I press the N key on the plugboard
    And I press the G key on the virtual keyboard
    Then The letter N should be displayed in the output box

 Scenario Outline: Plugboard reached its limits
  Given The Enigma Website is opened
   And I have a list of keys <keys>
  When I press on the specified keys on the plugboard
  And I press the K key on the plugboard
  Then an alert is shown

  Examples:
  |keys                                                      |
  |A, Z, B, Y, C, X, D, W, E, V, F, U, G, T, H, S, I, R, J, Q|


  Scenario: Plugboard Reset
    Given The Enigma Website is opened
    When I press the U key on the plugboard
    And I press the N key on the plugboard
    And I press the reset button on the plugboard
    And I press the G key on the virtual keyboard
    Then The letter U should be displayed in the output box


  Scenario: Plugboard Unset
    Given The Enigma Website is opened
    When I press the U key on the plugboard
    And I press the N key on the plugboard
    And I press the U key on the plugboard
    Then The plugboard box should be empty