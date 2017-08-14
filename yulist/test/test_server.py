import pytest

import yulist.admin


def test_index(browser):
    browser.open("/")
    assert "Welcome" in browser.page


def test_follow_links(browser):
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

    # Following navigation:
    music_link = browser.find_link("music")
    browser.click_link(music_link)
    assert "Music" in browser.page


def test_search_form(browser):
    browser.open("/search")
    assert "form" in browser.page


def test_perform_search(browser):
    browser.open("/search?pattern=bazel")
    assert "Search results" in browser.page
    assert "bazel.io" in browser.page
    page_link = browser.find_link("software/build/index")
    assert page_link


def test_when_not_logged_in_cannot_see_guilty_pleasures(browser):
    browser.open("video/series/index")
    assert "Guilty" not in browser.page
    print(browser.page)


def test_can_see_guilty_pleasures_when_logged_in(full_db, browser):
    yulist.admin.set_password(full_db, "admin", "p4ssw0rd")
    browser.open("/login")
    browser.submit_form("/login", username="admin", password="p4ssw0rd")
    assert "admin" in browser.page
    browser.open("video/series/index")
    assert "Guilty" in browser.page


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
