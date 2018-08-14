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

import click

from .github_trending import GithubTrending


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
    @click.argument('limit', required=False, default=10)
    @pass_github_trending
    def show(github_trending, limit):
        """Display Show Github trendings.

        Example(s):
            gt show
            gt show 5

        :type github_trending: :class:`github_treding.GithubTrending`
        :param github_trending: An instance of `github_trending.GithubTrending`.

        :type limit: int
        :param limit: specifies the number of items to show.
            Optional, defaults to 10.
        """
        github_trending.show(limit)
