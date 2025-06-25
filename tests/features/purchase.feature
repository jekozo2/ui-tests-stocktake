@use_store_state
Feature: Purchase functionalities
  As a stocktake user
  I want to be able to get, create, edit, delete purchases

  Background:
    Given user is on dashboard page

  @smoke @create_purchase
  Scenario: Create new purchase order
    Given 2 products are created
    And the user opens the new purchase order modal
    When the user populates all Purchase Order fields
    And the user submits the Purchase Order
    Then the new Purchase Order is created successfully

  @smoke @draft_purchase
  Scenario: Create new purchase order as Draft Purchase
    Given 2 products are created
    And the user opens the new purchase order modal
    When the user populates all Purchase Order fields
    And the user saves the Purchase Order as Draft
    Then the new Purchase Order is successfully saved as Draft

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

  Scenario: Item can be deleted during purchase creation
    Given 2 products are created
    And the user opens the new purchase order modal
    And the user populates all Purchase Order fields
    When the user deletes an Added Item from the Items List
    Then the item has been deleted successfully

  @negative @create_purchase
  Scenario: New purchase order not created without reference
    Given 2 products are created
    And the user opens the new purchase order modal
    When the user populates all Purchase Order fields without reference
    And the user submits the Purchase Order
    Then Purchase Order not created with error message: Purchase reference (invoice number) is required
    And there is no Purchase Order without reference in Purchase Order History Page
