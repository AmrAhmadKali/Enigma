Feature: Keyboard

  Scenario: Physical Keyboard is used as Enigma input
    Given The Enigma Website is opened
      When I press the G key on the PHYSICAL keyboard
      Then The letter G should be displayed in the INPUT box
      And The letter ? should be displayed in the OUTPUT box

  Scenario: Virtual Keyboard is used as Enigma input
    Given The Enigma Website is opened
      When I press the G key on the VIRTUAL keyboard
      Then The letter G should be displayed in the INPUT box
      And The letter ? should be displayed in the OUTPUT box
