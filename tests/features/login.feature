Feature: Login to Stocktake App

  Scenario: Successful Login
    Given user is on login page
    When the user provides correct credentials
    Then the user is successfully signed into the Stocktake app


  Scenario Outline: Failed Login with invalid credentials - <invalid_field>
    Given user is on login page
    When the user provides invalid credentials - <invalid_field>
    Then the login attempted has failed
    Examples:
      | invalid_field |
      | email         |
      | password      |
