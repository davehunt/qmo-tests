#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests
from unittestzero import Assert

from pages.link_crawler import LinkCrawler
from pages.home import HomePage


class TestEventsPage:

    link_check_url = '/category/events'
    link_check_locator = '#content a[href*="mozilla.org"]'

    @pytest.mark.nondestructive
    @pytest.mark.skip_selenium
    def test_events_page_links(self, link):
        Assert.equal(requests.get(link, verify=False).status_code, requests.codes.ok)

    @pytest.mark.nondestructive
    def test_events_title(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_home_page()
        events_page = home_page.header_region.click_events_link()
        Assert.true(events_page.is_the_current_page)
