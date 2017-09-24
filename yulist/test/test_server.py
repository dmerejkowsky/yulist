import pytest

import yulist.admin


@pytest.fixture
def logged_in_user(full_db, browser):
    yulist.admin.set_password(full_db, "admin", "p4ssw0rd")
    browser.open("/login")
    browser.submit_form("/login", username="admin", password="p4ssw0rd")


def test_index(browser, logged_in_user):
    browser.open("/")
    assert "Welcome" in browser.page


def test_follow_links(browser, logged_in_user):
    # Following table of contents
    browser.open("/index")
    assert "Welcome" in browser.page
    music_link = browser.find_link("Music")
    assert "Music" in browser.page
    browser.click_link(music_link)
    assert "Cover" in browser.page
    covers_link = browser.find_link("Cover songs")
    browser.click_link(covers_link)
    assert "favorites" in browser.page
    assert "Nina Simone" in browser.page

    # Following navigation:
    music_link = browser.find_link("music")
    browser.click_link(music_link)
    assert "Music" in browser.page


def test_search_form(browser, logged_in_user):
    browser.open("/search")
    assert "form" in browser.page


def test_perform_search(browser, logged_in_user):
    browser.open("/search?pattern=bazel")
    assert "Search results" in browser.page
    assert "bazel.io" in browser.page
    page_link = browser.find_link("software/index")
    assert page_link


def test_can_login_logout(full_db, browser):
    yulist.admin.set_password(full_db, "admin", "p4ssw0rd")
    browser.open("/login")
    browser.submit_form("/login", username="admin", password="p4ssw0rd")
    assert "admin" in browser.page
    logout_link = browser.find_link("logout")
    browser.click_link(logout_link)
    assert "admin" not in browser.page


def test_login_wrong_password(full_db, browser):
    yulist.admin.set_password(full_db, "admin", "p4ssw0rd")
    browser.open("/login")
    browser.submit_form("/login", username="admin", password="Inv4l1d")
    assert "Invalid password" in browser.page


def test_login_no_such_user(full_db, browser):
    yulist.admin.set_password(full_db, "admin", "p4ssw0rd")
    browser.open("/login")

    browser.submit_form("/login", username="nosuchuser", password="p4ssw0rd")
    assert "User not found" in browser.page


def test_not_found(full_db, client, logged_in_user):
    response = client.get("/nosuch")
    assert response.status_code == 404
    assert "not found" in response.data.decode()
