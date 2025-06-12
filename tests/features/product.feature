Feature: Product functionalities
  As a stocktake user
  I want to be able to create, edit, delete products, suppliers, item types, units and groups
  So that I can use them further in the stocktake app

  Background:
    Given user is on dashboard page

  @use_store_state
  Scenario: Create new stock item type
    Given the user navigates to create New Type from the New Product module
    When the user submits the type form after filling correctly all required fields
    Then the new type has been created successfully

  @use_store_state
  Scenario: Create new stock item unit
    Given the user navigates to create New Unit from the New Product module
    When the user submits the unit form after filling correctly all required fields
    Then the new unit has been created successfully

  @use_store_state
  Scenario: Create new stock item group
    Given the user navigates to create New Group from the New Product module
    When the user submits the group form after filling correctly all required fields
    Then the new group has been created successfully

  @use_store_state
  Scenario: Create new stock supplier
    Given the user navigates to create New Supplier from the New Product module
    When the user submits the supplier form after filling correctly all required fields
    Then the new supplier has been created successfully
