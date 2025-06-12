Feature: Main dashboard functionalities

  @use_store_state
  Scenario: All dashboard sections enabled
    Given user is on dashboard page
    When the user inspects the following sections
    Then they are all visible and enabled