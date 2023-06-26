Feature: Lamp panel

  Scenario: Lamp panel displays cipher text after virtual keypress
    Given The Enigma Website is opened
    When I press the G key on the virtual keyboard
    Then The lamp U lights up


  Scenario: Lamp panel displays cipher text after physical keypress
    Given The Enigma Website is opened
    When I press the U key on the physical keyboard
    Then The lamp G lights up
