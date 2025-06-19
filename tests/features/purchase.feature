Feature: Purchase functionalities
  As a stocktake user
  I want to be able to get, create, edit, delete purchases

  Background:
    Given user is on dashboard page

  @use_store_state
  Scenario: Create new purchase order
    Given 2 products are created
    And the user opens the new purchase order modal
    When the user populates all Purchase Order fields
    Then the new Purchase Order is created successfully
