import pytest


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
