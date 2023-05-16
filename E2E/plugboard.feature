Feature: Plugboard

  Scenario: Plugboard Set
    Given The Enigma Website is opened
    When I press the U key on the plugboard
    And I press the N key on the plugboard
    And I press the G key on the virtual keyboard
    Then The letter N should be displayed in the output box

  Scenario: Plugboard Reset
    Given The Enigma Website is opened
    When I press the U key on the plugboard
    And I press the N key on the plugboard
    And I press the reset button on the plugboard
    And I press the G key on the virtual keyboard
    Then The letter U should be displayed in the output box

# Auskommentieren sobald es funktioniert

#  Scenario: Plugboard Unset
#    Given The Enigma Website is opened
#    When I press the U key on the plugboard
#    And I press the N key on the plugboard
#    And I press the U key on the plugboard
#    And I press the G key on the physical keyboard
#    Then The letter U should be displayed in the output box