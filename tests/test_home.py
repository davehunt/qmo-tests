#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests
from unittestzero import Assert

from pages.home import HomePage
from pages.not_found import NotFoundPage
from pages.link_crawler import LinkCrawler


class TestHomePage:

    link_check_url = '/'
    link_check_locator = '#content a'

    @pytest.mark.nondestructive
    @pytest.mark.skip_selenium
    def test_home_page_links(self, link):
        Assert.equal(requests.get(link, verify=False).status_code, requests.codes.ok)

    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_that_favicon_present(self, mozwebqa):

        home_page = HomePage(mozwebqa)
        favicon_url = home_page.favicon_url
        r = requests.get(favicon_url, verify=False)

        Assert.equal(
            r.status_code, 200,
            u'request to %s responded with %s status code' % (favicon_url, r.status_code))

    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_that_robots_txt_present(self, mozwebqa):

        home_page = HomePage(mozwebqa)
        robots_url = u'%s/%s' % (home_page.base_url, 'robots.txt')
        r = requests.get(robots_url, verify=False)

        Assert.equal(
            r.status_code, 200,
            u'request to %s responded with %s status code' % (robots_url, r.status_code))

    @pytest.mark.nondestructive
    def test_that_proper_404_error_page_displayed(self, mozwebqa):

        not_found_page = NotFoundPage(mozwebqa)
        not_found_page.go_to_not_found_page()

        Assert.equal(not_found_page.page_title, u'Sorry, we couldn’t find that')

        Assert.equal(not_found_page.get_page_status_code(), 404,
                     u'GET request to this page should return 404 status code')

        err_msg_parts = []
        err_msg_parts.append(u'We looked everywhere, but we couldn’t find the page or file you were looking for. A few possible explanations:')
        err_msg_parts.append(u'You may have followed an out-dated link or bookmark.')
        err_msg_parts.append(u'If you entered the address by hand, you might have mistyped it.')
        err_msg_parts.append(u'Maybe you found a bug. Good work!')
        error_message = '\n'.join(err_msg_parts)

        Assert.equal(not_found_page.error_message, error_message)

    @pytest.mark.nondestructive
    def test_paginator(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_home_page()

        expected_page = 1

        # On the first page, "previous" is not active, and the page url is the home_page
        Assert.true(home_page.is_the_current_page)
        Assert.false(home_page.paginator.is_prev_page_visible)
        Assert.equal(home_page.paginator.page_number, expected_page)
        Assert.true(home_page.paginator.is_next_page_visible)
        Assert.contains('This is\nPage %s of' % home_page.paginator.current_page_number, home_page.paginator.page_x_of_y_message)

        # Move forward one page by clicking next
        home_page.paginator.click_next_page()

        # Move 5 pages to the right
        pages_to_test = 5 if home_page.paginator.total_page_number >= 5 else home_page.paginator.total_page_number
        for i in range(1, pages_to_test):
            Assert.true(home_page.paginator.is_next_page_visible)
            Assert.true(home_page.get_url_current_page().endswith('%s/' % home_page.paginator.page_number))
            Assert.contains('This is\nPage %s of' % home_page.paginator.current_page_number, home_page.paginator.page_x_of_y_message)
            Assert.equal(home_page.paginator.page_number, home_page.paginator.current_page_number)
            home_page.paginator.click_next_page()

        # Move 5 pages to the left
        for i in range(1, pages_to_test):
            Assert.true(home_page.paginator.is_prev_page_visible)
            Assert.true(home_page.get_url_current_page().endswith('%s/' % home_page.paginator.page_number))
            Assert.contains('This is\nPage %s of' % home_page.paginator.current_page_number, home_page.paginator.page_x_of_y_message)
            Assert.equal(home_page.paginator.page_number, home_page.paginator.current_page_number)
            home_page.paginator.click_prev_page()

        # Click last page. "previous" is active, but "next" is not
        expected_page = home_page.paginator.total_page_number

        home_page.paginator.click_last_page()

        Assert.true(home_page.paginator.is_prev_page_visible)
        Assert.false(home_page.paginator.is_next_page_visible)
        Assert.equal(home_page.paginator.page_number, expected_page)
        Assert.true(home_page.get_url_current_page().endswith('%s/' % home_page.paginator.page_number))
        Assert.contains('This is\nPage %s of' % home_page.paginator.current_page_number, home_page.paginator.page_x_of_y_message)

        # Click a middle page from the shown list
        home_page.paginator.click_middle_page()

        Assert.true(home_page.paginator.is_next_page_visible)
        Assert.true(home_page.get_url_current_page().endswith('%s/' % home_page.paginator.page_number))
        Assert.contains('This is\nPage %s of' % home_page.paginator.current_page_number, home_page.paginator.page_x_of_y_message)
        Assert.equal(home_page.paginator.page_number, home_page.paginator.current_page_number)
