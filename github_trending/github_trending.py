# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
# Modifications copyright 2018 Yuya Chiba.
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

from .config import Config
from .lib.github.github import GithubTrendingApi
from .lib.mdv import markdownviewer as mdv
#from .lib.pretty_date_time import pretty_date_time
#from .onions import onions
#from .web_viewer import WebViewer
#from .completions import SUBCOMMANDS, ARGS_OPTS_LOOKUP


class GithubTrending(object):
    """Encapsulate Github Trending."""

    MAX_COLUMN = 100

    def __init__(self):
        self.github_trending_api = GithubTrendingApi()
        self.config = Config()
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
        click.secho('Item with id {0} not found.'.format(item_id), fg=self.config.clr_error)

    def get_east_asian_width_count(self, text):
        count = 0
        for c in text:
            if unicodedata.east_asian_width(c) in 'FWA':
                count += 2
            else:
                count += 1
        return count

    def format_repository(self, index, repository):

        def _get_blank_num(repository):
            """ Gets the blank num of between fork to today stars.
            """
            blank_num = self.MAX_COLUMN
            blank_num -= 6 # header blanks
            if repository['Programming Language']:
                blank_num -= len(repository['Programming Language']) + 4 # a 2 byte unicode and 2 blanks
            if repository['Total stars']:
                blank_num -= len(repository['Total stars']) + 4 # a 2 byte unicode and 2 blanks
            if repository['Forks']:
                blank_num -= len(repository['Forks']) + 3 # a 2 byte unicode and a blank
            blank_num -= len(repository['Stars trending']) + 3 # a 2 byte unicode and 2 blanks
            return blank_num

        def _is_description_english(s):
            for c in s:
                if unicodedata.east_asian_width(c) in 'FWA':
                    return False
            return True

        def _is_word_one_language(text):
            text_len = self.get_east_asian_width_count(text)
            if text_len == len(text) or text_len == len(text) * 2:
                return True
            else:
                return False

        def _format_description(description):
            formatted_description = ''
            max_column = 78 # for description
            column_len = 6 # header blanks

            for word in description.split(' '):
                if _is_description_english(word):
                    if column_len + len(word) > max_column:
                        formatted_description += '\n      '
                        column_len = 6
                for c in word:
                    column_len += self.get_east_asian_width_count(c)
                    if column_len > max_column:
                        formatted_description += '\n      '
                        column_len -= max_column
                    formatted_description += c
                formatted_description += ' '
                column_len += 1
            return formatted_description

        def _format_programming_language(programming_language):
            if programming_language:
                return u'\U0001F4D6 ' + programming_language + '  '
            else:
                return ''

        def _format_total_stars(total_stars):
            if total_stars:
                return u'\U00002B50 ' + total_stars + '  '
            else:
                return ''

        def _format_forks(forks):
            if forks:
                return u'\U0001F374 ' + forks
            else:
                return ''

        formatted_repository  = click.style('  {0}.'.format(str(index)), fg=self.config.clr_view_index)
        formatted_repository += ' ' * (3-len(str(index)))
        formatted_repository += click.style(repository['User'] + '/', fg=self.config.clr_user)
        formatted_repository += click.style(repository['Repository'] + '\n      ', fg=self.config.clr_rep_repository, bold=True)
        description = _format_description(repository['Description'])
        formatted_repository += click.style(description + '\n      ', fg=self.config.clr_description)
        programming_language  = _format_programming_language(repository['Programming Language'])
        formatted_repository += click.style(programming_language, fg=self.config.clr_programming_language)
        total_stars           = _format_total_stars(repository['Total stars'])
        formatted_repository += click.style(total_stars, fg=self.config.clr_total_stars)
        forks                 = _format_forks(repository['Forks'])
        formatted_repository += click.style(forks, fg=self.config.clr_forks)
        formatted_repository += ' ' * _get_blank_num(repository)
        formatted_repository += click.style(u'\U00002B50 ' + repository['Stars trending'] + '\n', fg=self.config.clr_total_stars)
        return formatted_repository

    def format_developer(self, index, developer):

        def _get_owner_and_organization(developer_name):
            developer_name = developer_name.split(' (')
            owner = developer_name[0].strip()
            try:
                organization = '(' + developer_name[1].strip()
            except IndexError:
                organization = ''
            return owner, organization

        def _format_description(repository, description):
            formatted_description = ''
            col = self.MAX_COLUMN - self.get_east_asian_width_count(repository) - 6 - 4
            for c in description:
                if col < 4:
                    formatted_description += '.' * col
                    break
                else:
                    formatted_description += c
                col -= self.get_east_asian_width_count(c)
            return formatted_description

        formatted_developer  = click.style('  {0}.'.format(str(index)), fg=self.config.clr_view_index)
        formatted_developer += ' ' * (3-len(str(index)))
        owner, organization  = _get_owner_and_organization(developer['Developer'])
        formatted_developer += click.style(owner + ' ', fg=self.config.clr_owner, bold=True)
        formatted_developer += click.style(organization + '\n      ', fg=self.config.clr_organization, bold=True)
        formatted_developer += click.style(u'\U0001F516  ' + developer['Repository'] + ' ', fg=self.config.clr_dev_repository)
        description          = _format_description(developer['Repository'], developer['Description'])
        formatted_developer += click.style(description + '\n', fg=self.config.clr_description)
        return formatted_developer

    def tip_view(self):
         """Create the tip about the view command."""
         tip = click.style('  Tip: View the README for repository with the following command:\n', fg=self.config.clr_general)
         tip += click.style('    gt view [user/repository] ', fg=self.config.clr_view_index)
         tip += click.style('optional: [-b/--browser] [--help]\n', fg=self.config.clr_tooltip)
         return tip

    def print_repository_not_found(self):
        pass

    def print_developer_not_found(self):
        pass

    def print_repository(self, repositories):
        self.config.repositories = {}
        for index, repository in repositories.items():
            try:
                formatted_repository = self.format_repository(index, repository)
                click.echo(formatted_repository)
                user_repository = repository['User'] + '/' + repository['Repository']
                self.config.repositories[user_repository] = repository['Description']
            except:
                self.print_repository_not_found()
        self.config.save_cache()
        if self.config.show_tip:
            click.secho(self.tip_view())

    def print_developer(self, developers):
        self.config.repositories = {}
        for index, developer in developers.items():
            try:
                formatted_developer = self.format_developer(index, developer)
                click.echo(formatted_developer)
                developer_repository = developer['Developer'].split(' (')[0] + \
                                       '/' + developer['Repository']
                self.config.repositories[developer_repository] = developer['Description']
            except:
                self.print_developer_not_found()
        self.config.save_cache()


    def trend(self, language, dev, weekly, monthly, browser, limit):
        """Display Github Trendings.

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
            click.secho('\nOpening ' + url + ' ...\n', fg=self.config.clr_general)
            webbrowser.open(url)
        else:
            result = self.github_trending_api.get_metadata(language, dev, weekly, monthly, limit)
            if dev:
                self.print_developer(result)
            else:
                self.print_repository(result)

    def view(self, repository, browser):
        """Display View repository README."""
        if browser:
            url = 'https://github.com/' + repository
            click.secho('\nOpening ' + url + ' ...\n', fg=self.config.clr_general)
            webbrowser.open(url)
        else:
            for md in ['README.md', 'README.rst', 'README.txt', 'README']:
                url = 'https://raw.githubusercontent.com/' + repository + '/master/' + md
                res = requests.get(url, stream=True)
                if res.status_code == 200:
                    click.secho('\nOpening ' + url + ' ...\n', fg=self.config.clr_general)
                    header = click.style('Viewing ' + url + '\n', fg=self.config.clr_general)
                    content = mdv.main(md=res.text, L=True, l=True)
                    click.echo_via_pager(header + content)
                    return
            click.secho('Error: ' + repository + ' is not found.', fg=self.config.clr_error)


