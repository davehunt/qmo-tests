#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests
from unittestzero import Assert

from pages.home import HomePage


class TestMediaPage:

    link_check_url = '/media'
    link_check_locator = '#content-main a'

    @pytest.mark.nondestructive
    @pytest.mark.skip_selenium
    def test_media_page_links(self, link):
        Assert.equal(requests.get(link, verify=False).status_code, requests.codes.ok)

    @pytest.mark.nondestructive
    def test_media_title(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_home_page()
        media_page = home_page.header_region.click_media_link()
        Assert.true(media_page.is_the_current_page)
