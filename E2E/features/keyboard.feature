Feature: Keyboard

  Scenario: Physical Keyboard is used as Enigma input
    Given The Enigma Website is opened
      When I press the G key on the physical keyboard
      Then The letter G should be displayed in the input box
      And The letter ? should be displayed in the output box

  Scenario: Virtual Keyboard is used as Enigma input
    Given The Enigma Website is opened
      When I press the G key on the virtual keyboard
      Then The letter G should be displayed in the input box
      And The letter ? should be displayed in the output box
