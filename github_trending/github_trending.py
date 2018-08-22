# -*- coding: utf-8 -*-

# Copyright 2018 Yuya Chiba. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from __future__ import print_function
from __future__ import division

import platform
import re
import sys
import webbrowser
import unicodedata
import requests

import click
#from .compat import HTMLParser
#from .compat import urlparse

##rom .config import Config
from .lib.github.github import GithubTrendingApi
from .lib.mdv import markdownviewer as mdv
#from .lib.pretty_date_time import pretty_date_time
#from .onions import onions
#from .web_viewer import WebViewer
#from .completions import SUBCOMMANDS, ARGS_OPTS_LOOKUP


class GithubTrending(object):
    """Encapsulate Github Trending."""

    MAX_LIST = 10000;

    def __init__(self):
        self.github_trending_api = GithubTrendingApi()
        # self.config = Config()
        # self.web_viewer = WebViewer()

    def headlines_message(self, message):
        """Create the "Fetching [message] Headlines..." string.

        :type message: str
        :param message: The headline message.

        :rtype: str
        :return: "Fetching [message] Headlines...".
        """
        return 'Fetching {0} Headlines...'.format(message)

    def print_item_not_found(self, item_id):
        """Print a message the given item id was not found.

        :type item_id: int
        :param item_id: The item's id.
        """
        click.secho('Item with id {0} not found.'.format(item_id), fg='red')

    def format_repository(self, index, repository):

        def _get_blank_num(formatted_repository):
            """ Gets the blank num of between fork to today stars.
            """
            max_column = 100
            blank_num = max_column - len(formatted_repository[formatted_repository.rfind('\n'):])
            return blank_num

        def _get_east_asian_width_count(text):
            count = 0
            for c in text:
                if unicodedata.east_asian_width(c) in 'FWA':
                    count += 2
                else:
                    count += 1
            return count

        def _is_description_english(s):
            for c in s:
                if unicodedata.east_asian_width(c) in 'FWA':
                    return False
            return True

        def _is_word_one_language(text):
            text_len = _get_east_asian_width_count(text)
            if text_len == len(text) or text_len == len(text) * 2:
                return True
            else:
                return False

        def _format_description(description):
            max_column = 78
            description_char_num = _get_east_asian_width_count(description)
            if description_char_num <= max_column:
                return description

            formatted_description = ''
            column_len = 0

            word_list = description.split(' ')
            for word in word_list:
                if _is_description_english(word):
                    if column_len + len(word) > max_column:
                        formatted_description += '\n      '
                        column_len = 0
                for c in word:
                    column_len += _get_east_asian_width_count(c)
                    if column_len > max_column:
                        formatted_description += '\n      '
                        column_len -= max_column
                    formatted_description += c
                formatted_description += ' '
                column_len += 1
            return formatted_description

        formatted_repository  = click.style('  {0}.'.format(str(index)), fg='magenta') + ' ' * (3-len(str(index)))
        formatted_repository += click.style(repository['User'] + '/', fg='cyan')
        formatted_repository += click.style(repository['Repository'], fg='cyan', bold=True)
        formatted_repository += '\n      '
        try:
            formatted_repository += _format_description(repository['Description'])
        except:
            # Description is none
            pass
        formatted_repository += '\n      '
        try:
            formatted_repository += click.style(u'\U0001F4D6 ' + repository['Programming Language'] + '  ', fg='red')
        except:
            # Programming language is none
            formatted_repository += click.style('', fg='red')
        try:
            formatted_repository += click.style(u'\U00002B50 ' + repository['Total stars'] + '  ', fg='yellow')
        except:
            # Total stars is none
            formatted_repository += click.style('', fg='yellow')
        try:
            formatted_repository += click.style(u'\U0001F374 ' + repository['Forks'], fg='green')
        except:
            formatted_repository += click.style('', fg='green')
        finally:
            formatted_repository += ' ' * _get_blank_num(formatted_repository)
            formatted_repository += click.style(u'\U00002B50 ' + repository['Stars trending'], fg='yellow')
            formatted_repository += '\n'
            return formatted_repository

    def format_developer(self, index, developer):
        formatted_developer  = ''
        formatted_developer  = click.style('{0}.'.format(str(index)), fg='magenta') + ' ' * (3-len(str(index)))
        developer_name = developer['Developer']
        try:
            i = developer_name.index('(')
        except:
            i = len(developer_name)
        formatted_developer += click.style(developer_name[:i], fg='cyan', bold=True)
        formatted_developer += click.style(developer_name[i:], fg='green', bold=True)
        formatted_developer += '\n    '
        formatted_developer += click.style(u'\U0001F516  ' + developer['Repository'])
        formatted_developer += '\n'
        return formatted_developer


    def print_repository_not_found(self):
        pass

    def print_developer_not_found(self):
        pass

    def print_repository(self, repositories):
        # TODO: save_cache
        for index, repository in repositories.items():
            try:
                formatted_repository = self.format_repository(index, repository)
                click.echo(formatted_repository)
            except:
                self.print_repository_not_found()

    def print_developer(self, developers):
        # TODO: save_cache
        for index, developer in developers.items():
            try:
                formatted_developer = self.format_developer(index, developer)
                click.echo(formatted_developer)
            except:
                self.print_developer_not_found()

    def tip_view(self):
         """Create the tip about the view command."""
         tip = click.style('  Tip: View the README for repository with the following command:\n', fg='white')
         tip += click.style('    gt view [user/repository] ', fg='magenta')
         tip += click.style('optional: [-b/--browser] [--help]\n')
         return tip

    def show(self, language, dev, weekly, monthly, browser, limit):
        """Display Show Github Trendings.

        :type dev: bool
        :param dev: Determines whether to show Developers Trendings.

        :type limit: int
        :param limit: the number of repositories to show, optional. defaults to 10.
        """
        def _create_url(language, dev, weekly, monthly):
            url = 'https://github.com/trending'
            if dev:
                url += '/developers'
            if language:
                url += '/' + language
            if weekly:
                url += '?since=weekly'
            elif monthly:
                url += '?since=monthly'
            return url

        if browser:
            url = _create_url(language, dev, weekly, monthly)
            click.secho('\nOpening ' + url + ' ...\n', fg='white')
            webbrowser.open(url)
        else:
            result = self.github_trending_api.get_metadata(language, dev, weekly, monthly, limit)
            if dev:
                self.print_developer(result)
            else:
                self.print_repository(result)
                click.secho(self.tip_view())

    def view(self, repository, browser):
        """Display View repository README."""
        if browser:
            url = 'https://github.com/' + repository
            click.secho('\nOpening ' + url + ' ...\n', fg='white')
            webbrowser.open(url)
        else:
            for md in ['README.md', 'README.rst', 'README.txt', 'README']:
                url = 'https://raw.githubusercontent.com/' + repository + '/master/' + md
                res = requests.get(url, stream=True)
                if res.status_code == 200:
                    click.secho('\nOpening ' + url + ' ...\n', fg='white')
                    header = click.style('Viewing ' + url + '\n', fg='white')
                    content = mdv.main(md=res.text, L=True, l=True)
                    click.echo_via_pager(header + content)
                    return
            click.secho('Error: ' + repository + ' is not found.', fg='red')


