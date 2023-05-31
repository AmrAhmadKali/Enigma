Feature: Keyboard

  Scenario: Physical Keyboard is used as Enigma input
    Given The Enigma Website is opened
      When I press the G key on the physical keyboard
      Then The letter G should be displayed in the input box
      And The letter U should be displayed in the output box

  Scenario: Virtual Keyboard is used as Enigma input
    Given The Enigma Website is opened
      When I press the G key on the virtual keyboard
      Then The letter G should be displayed in the input box
      And The letter U should be displayed in the output box

  Scenario: Input history reaches 140 characters
    Given The Enigma Website is opened
    When I press the G key 140 times on the keyboard
    And I press the G key on the virtual keyboard
    Then I see only 140 characters in the input box
    And I see only 140 characters in the output box