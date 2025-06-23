@use_store_state
Feature: Purchase functionalities
  As a stocktake user
  I want to be able to get, create, edit, delete purchases

  Background:
    Given user is on dashboard page

  Scenario: Create new purchase order
    Given 2 products are created
    And the user opens the new purchase order modal
    When the user populates all Purchase Order fields
    And the user submits the Purchase Order
    Then the new Purchase Order is created successfully

  Scenario: Unify same items on new purchase order
    Given 2 identical products are created
    And 1 another product is created
    And the user opens the new purchase order modal
    When the user populates all Purchase Order fields
    And the user checks the 'Unify same items' checkbox
    Then the same items are merged into one

  Scenario: Item can be edited during purchase creation
    Given 2 products are created
    And the user opens the new purchase order modal
    And the user populates all Purchase Order fields
    When the user edits the Added Item from the Items List
    Then the item values have been edited successfully