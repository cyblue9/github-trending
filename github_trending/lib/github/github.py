# -*- coding: utf-8 -*-

# MIT License
#
# Copyright(c) 2017 Evyatar Meged
# Modifications copyright 2018 Yuya Chiba.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import click
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Constants
ACCEPTED_LANGUAGES = [
    'javascript', 'python', 'java', 'ruby', 'php', 'c++', 'css', 'c#', 'go',
    'c', 'typescript', 'shell', 'swift', 'scala', 'objective-c', 'html',
    'rust', 'coffeescript', 'haskell', 'groovy', 'lua', 'elixir',
    'perl', 'kotlin', 'clojure'
]

# Repository information parsing functions
class GithubTrendingApi(object):
    """Encapsulate the Github Trending API."""

    def __init__(self):
        self.base_url = 'https://github.com/'
        self.trending_url = self.base_url + 'trending/'
        self.xml_declaration = '<?xml version="1.0" encoding="UTF-8" ?>\n'
        self.recode = '\t<record>\n'
        self.end_record = '\t</record>\n'
        self.item = '\t\t<{0}>{1}</{0}>\n'
        self.root = '<root>\n'
        self.end_root = '</root>'


    def username_and_reponame(self, repo_info):
        """Return user name and repository name"""
        try:
            data = repo_info.find('a').get('href').split('/')
            try:
                username = data[1]
            except IndexError:
                username = ''
            try:
                repo_name = data[2]
            except IndexError:
                repo_name = ''
            return username, repo_name
        except AttributeError:
            return '', ''


    def get_description(self, repo_info):
        """Return repository description"""
        try:
            return repo_info.find('p').text.strip()
        except AttributeError:
            return ''


    def get_programming_language(self, repo_info):
        """Return programming language used for repository"""
        try:
            return repo_info.find('span', {'itemprop': 'programmingLanguage'}).text.strip()
        except AttributeError:
            return ''


    def stars_and_forks(self, repo_info):
        """Return total stars and forks"""
        try:
            data = repo_info.select('a.muted-link')
            # Handle no stars/forks data on repo
            try:
                stars = data[0].text.strip()
            except IndexError:
                stars = ''
            try:
                forks = data[1].text.strip()
            except IndexError:
                forks = ''
            return stars, forks
        except AttributeError:
            return '', ''


    def get_stars_trending(self, repo_info):
        """Return stars trending"""
        try:
            return repo_info.find('span', {'class': 'float-sm-right'}).text.strip()
        except AttributeError:
            return ''


    def parse_repositories_info(self, tag, limit):
        """
        Scrape trending repository info
        :return A dictionary of all trending repositories filtered by arguments from user
        """
        trending = {}
        for content in tag:
            repositories = content.find_all('li')
            for index, list_item in enumerate(repositories, start=1):
                username, repo_name = self.username_and_reponame(list_item)
                stars, forks = self.stars_and_forks(list_item)
                trending[index] = {
                    'User': username,
                    'Repository': repo_name,
                    'URL': self.base_url + '/'.join((username, repo_name)),
                    'Description': self.get_description(list_item),
                    'Programming Language': self.get_programming_language(list_item),
                    'Total stars': stars,
                    'Forks': forks,
                    'Stars trending': self.get_stars_trending(list_item)
                }
                if index >= limit:
                    return trending
        return trending


    # END Repository parsing functions


    # Developer information parsing functions

    def get_developer(self, repo_info):
        """Get trending developer name"""
        try:
            developer = ' '.join(repo_info.find('h2').find('a').text.split())
            return developer
        except AttributeError:
            return ''


    def get_profile(self, repo_info):
        """Get trending developer profile url"""
        try:
            profile = self.base_url + repo_info.find('h2').find('a').get('href')
            return profile
        except AttributeError:
            return ''


    def get_developer_repo(self, item):
        """
        Get the repository that made the developer trending
        :return repository name and url
        """
        try:
            a = item.find('a', {'class': 'repo-snipit'})
            url = self.base_url + a.get('href').strip()
            repo_name = a.find('span').text.strip()
            return repo_name, url
        except AttributeError:
            return '', ''

    def get_developer_repo_description(self, item):
        """Get trending develoer repository description"""
        try:
            description = item.find(class_='repo-snipit-description css-truncate-target').text.strip()
            return description
        except AttributeError:
            return ''

    def parse_developers_info(self, tag, limit):
        """
        Scrape trending developer info
        :return A dictionary with all trending developers filtered by arguments from user
        """
        trending = {}
        for content in tag:
            repositories = content.find_all('li')
            for index, list_item in enumerate(repositories, start=1):
                repo_name, url = self.get_developer_repo(list_item)
                description = self.get_developer_repo_description(list_item)
                trending[index] = {
                    'Developer': self.get_developer(list_item),
                    'Profile': self.get_profile(list_item),
                    'Repository': repo_name,
                    'URL': url,
                    'Description': description
                }
                if index >= limit:
                    return trending
        return trending


    # END Developer parsing functions


    # All around functions

    def make_connection(self, url):
        """Establish connection with url"""
        page = requests.get(url)
        if page.status_code != 200:
            if page.status_code == 429:
                click.secho('Error: Too many requests', fg='red')
            else:
                click.secho('Error: Could not establish connection with GitHub', fg='red')
            exit(1)
        return page


    def add_duration_query(self, url, weekly=None, monthly=None):
        """Add duration according to arguments"""
        if weekly:
            url += '?since=weekly'
        elif monthly:
            url += '?since=monthly'
        return url


    def build_url(self, language=None, dev=False, monthly=False, weekly=False):
        """Build destination URL according to arguments"""
        url = self.trending_url
        if dev:
            url += '/developers/'
        if language:
            if language.lower() == 'c#':
                url += 'c%23'  # Handle C# url encoding
            else:
                url += language.lower()
        url = self.add_duration_query(url=url, weekly=weekly, monthly=monthly)
        return url


    def get_metadata(self, language, dev, weekly, monthly, limit):
        """Build URL, connect to page and create BeautifulSoup object, build and return result"""
        url = self.build_url(language=language, dev=dev, monthly=monthly, weekly=weekly)
        page = self.make_connection(url)
        soup = BeautifulSoup(page.text, 'lxml')
        explore_content = soup.select('.explore-content')
        if dev:
            result = self.parse_developers_info(explore_content, limit)
        else:
            result = self.parse_repositories_info(explore_content, limit)
        return result
