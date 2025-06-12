import logging

from playwright.sync_api import expect
from pytest_bdd import given, then, parsers, when, scenarios

from tests.conftest import ROOT_DIR

scenarios(ROOT_DIR / "tests" / "features" / "login.feature")


@given("user is on login page")
def dummy_test_step():
    logging.info("Into dummy test step without params.")


@when("the user provides correct credentials")
def submit_login_with_correct_credentials(login_page, credentials):
    logging.info("Submit login with correct credentials")
    (
        login_page
        .populate_email_field_with(credentials['email'])
        .populate_password_field_with(credentials['password'])
        .submit_login_credentials()
    )


@when(parsers.parse("the user provides invalid credentials - {invalid_field}"))
def submit_login_with_incorrect_credentials(login_page, credentials, invalid_field):
    logging.info("Submit login with incorrect credentials")
    if invalid_field == 'email':
        (
            login_page
            .populate_email_field_with("invalid_user@gmail.com")
            .populate_password_field_with(credentials['password'])
            .submit_login_credentials()
        )
    if invalid_field == 'password':
        (
            login_page
            .populate_email_field_with(credentials['email'])
            .populate_password_field_with("invalid!")
            .submit_login_credentials()
        )


@then("the user is successfully signed into the Stocktake app")
def validate_successful_login(login_page):
    expect(login_page.content_user_email, "Home Page to display the user email").to_contain_text("test_user@gmail.com")


@then("the login attempted has failed")
def validate_failed_login(login_page):
    expect(login_page.login_error_message, "Login failed message to be displayed").to_contain_text("Login failed")
