from urlparse import urlparse
import requests
from unittestzero import Assert

from bs4 import BeautifulSoup


def pytest_generate_tests(metafunc):
    if 'link' in metafunc.fixturenames:
        url = '%s%s' % (metafunc.config.option.base_url, metafunc.cls.link_check_url)
        # TODO Add proxy support
        r = requests.get(url, verify=False)
        Assert.equal(r.status_code, requests.codes.ok,
                     '{0.url} returned: {0.status_code} {0.reason}'.format(r))

        parsed_html = BeautifulSoup(r.text)
        urls = [a['href'] for a in parsed_html.select(metafunc.cls.link_check_locator)]
        urls = map(lambda u: u if not u.startswith('/') else metafunc.config.option.base_url + u, urls)
        metafunc.parametrize('link', [u for u in urls if urlparse(u).scheme.startswith('http')])
