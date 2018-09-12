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

import click

from .github_trending import GithubTrending
from .lib.github.github import ACCEPTED_LANGUAGES


pass_github_trending = click.make_pass_decorator(GithubTrending)


class GithubTrendingCli(object):
    """Encapsulate the Github Trending Command Line Interface."""

    @click.group()
    @click.pass_context
    def cli(ctx):
        """Main entry point for GithubTrendingCli.

        :type ctx: :class:`click.core.Context`
        :param ctx: An instance of click.core.Context that stores an instance
            of `github_trending.GtihubTrending`.
        """
        # Create a GithubTrending object and remember it as the context object.
        # From this point onwards other commands can refer to it by using the
        # @pass_github_trending decorator.
        ctx.obj = GithubTrending()

    @cli.command()
    @click.option('--language', '-la', help='View specific language trending')
    @click.option('--dev', '-d', is_flag=True, help='View developers trending')
    @click.option('--weekly', '-w', is_flag=True, help='View 1 week trending')
    @click.option('--monthly', '-m', is_flag=True, help='View 1 month trending')
    @click.option('--browser', '-b', is_flag=True, help='View in a browser instead of the terminal')
    @click.option('--limit', '-li', default=25, help='Limits the number of items displayed')
    @pass_github_trending
    def trend(github_trending, language, dev, weekly, monthly, browser, limit):
        """Display Github trendings.

        Example(s):
            gt trend
            gt trend 5

        :type github_trending: :class:`github_treding.GithubTrending`
        :param github_trending: An instance of `github_trending.GithubTrending`.

        :type limit: int
        :param limit: specifies the number of items to show.
            Optional, defaults to 10.
        """
        if language and language.lower() not in ACCEPTED_LANGUAGES:
            click.secho('Error: Specified programming language not in supported languages')
            return
        if weekly and monthly:
            click.secho('Error: Please specify weekly OR monthly')
            return

        github_trending.trend(language, dev, weekly, monthly, browser, limit)

    @cli.command(help='View README of repository(ex:blue-9/github-trending)')
    @click.argument('repository')
    @click.option('--browser', '-b', is_flag=True, help='View in a browser instead of the terminal')
    @pass_github_trending
    def view(github_treding, repository, browser):
        """Display View repository README"""

        github_treding.view(repository, browser)
