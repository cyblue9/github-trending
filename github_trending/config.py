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

import os
import ast

import click
from .compat import configparser
from .compat import urlretrieve

class Config(object):
    """Github Trending config."""

    CONFIG = '.githubtrendingconfig'
    CONFIG_CLR_GENERAL = 'clr_general'
    CONFIG_CLR_TOOLTIP = 'clr_tooltip'
    CONFIG_CLR_ERROR = 'clr_error'
    CONFIG_CLR_VIEW_INDEX = 'clr_view_index'
    CONFIG_CLR_USER = 'clr_user'
    CONFIG_CLR_REP_REPOSITORY = 'clr_rep_repository'
    CONFIG_CLR_DESCRIPTION = 'clr_description'
    CONFIG_CLR_PROGRAMMING_LANGUAGE = 'clr_programming_language'
    CONFIG_CLR_TOTAL_STARS = 'clr_total_stars'
    CONFIG_CLR_FORKS = 'clr_forks'
    CONFIG_CLR_STARS_TRENDING = 'clr_stars_trending'
    CONFIG_CLR_OWNER = 'clr_owner'
    CONFIG_CLR_ORGANIZATION = 'clr_organization'
    CONFIG_CLR_DEV_REPOSITORY = 'clr_dev_repository'
    CONFIG_SECTION = 'github-trending'
    CONFIG_REPOSITORIES = 'repositories'
    CONFIG_SHOW_TIP = 'show_tip'
    MAX_ITEM_CACHE_SIZE = 20000

    def __init__(self):
        self.repositories = {}
        self.show_tip = True
        self._init_colors()
        self.load_config([
            self.load_config_repositories,
            self.load_config_colors,
            self.load_config_show_tip,
        ])

    def _init_colors(self):
        """Initialize colors to their defaults."""
        self.clr_general = 'white'
        self.clr_tooltip = 'white'
        self.clr_error = 'red'
        self.clr_view_index = 'magenta'
        self.clr_user = 'cyan'
        self.clr_rep_repository = 'cyan'
        self.clr_description = 'white'
        self.clr_programming_language = 'red'
        self.clr_total_stars = 'yellow'
        self.clr_forks = 'green'
        self.clr_stars_trending = 'yellow'
        self.clr_owner = 'cyan'
        self.clr_organization = 'green'
        self.clr_dev_repository = 'yellow'

    def clear_repositories(self):
        """Clear the repository cache."""
        self.repositories = {}
        self.save_cache()

    def get_config_path(self, config_file_name):
        """Get the config file path.

        :type config_file_name: str
        :param config_file_name: The config file name.

        :rtype: str
        :return: The config file path.
        """
        home = os.path.abspath(os.getenv('HOME', ''))
        config_file_path = os.path.join(home, config_file_name)
        return config_file_path

    def load_config(self, config_funcs):
        """Load the specified config from ~/.guthubtrendingconfing.

        :type config_funcs: list
        :param config_funcs: The config functions to run.
        """
        config_file_path = self.get_config_path(self.CONFIG)
        parser = configparser.RawConfigParser()
        try:
            with open(config_file_path) as config_file:
                try:
                    parser.read_file(config_file)
                except AttributeError:
                    parser.readfp(config_file)
                for config_func in config_funcs:
                    config_func(parser)
        except IOError:
            # There might not be a cache yet, just silently return.
            return None

    def load_config_colors(self, parser):
        """Load the color config from ~/.githubtrending.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.load_colors(parser)

    def load_config_repositories(self, parser):
        """Load the repository cache from ~/.githubtrendingconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.repositories = self.load_section_list(parser,
                                                   self.CONFIG_REPOSITORIES)

    def load_config_show_tip(self, parser):
        """Load the show tip config from ~/.githubtrendingconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instace of `ConfigParser.RawConfigParser`.
        """
        self.show_tip = parser.getboolean(self.CONFIG_SECTION,
                                          self.CONFIG_SHOW_TIP)

    def load_color(self, parser, color_config, default):
        """Load the specified color form ~/.githubtrendingconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.

        :type color_config: str
        :param color_config: The color config label to load.

        :type default: str
        :param default: The default color if no color config exists.
        """
        try:
            color = parser.get(self.CONFIG_SECTION, color_config)
            if color == 'none':
                color = None
            # Check if the user input a valid color.
            # If invalid, this will throw a TypeError
            click.style('', fg=color)
        except (TypeError, configparser.NoOptionError):
            return default
        return color

    def load_colors(self, parser):
        """Load all colors from ~/.githubtrendingconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.
        """
        self.clr_general = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_GENERAL,
            default=self.clr_general)
        self.clr_tooltip = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_TOOLTIP,
            default=self.clr_tooltip)
        self.clr_error = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_ERROR,
            default=self.clr_error)
        self.clr_view_index = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_VIEW_INDEX,
            default=self.clr_view_index)
        self.clr_user = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_USER,
            default=self.clr_user)
        self.clr_rep_repository = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_REP_REPOSITORY,
            default=self.clr_rep_repository)
        self.clr_description = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_DESCRIPTION,
            default=self.clr_description)
        self.clr_programming = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_PROGRAMMING_LANGUAGE,
            default=self.clr_programming_language)
        self.clr_total_stars = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_TOTAL_STARS,
            default=self.clr_total_stars)
        self.clr_forks = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_FORKS,
            default=self.clr_forks)
        self.clr_stars_trending = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_STARS_TRENDING,
            default=self.clr_stars_trending)
        self.clr_owner = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_OWNER,
            default=self.clr_owner)
        self.clr_organization = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_ORGANIZATION,
            default=self.clr_organization)
        self.clr_dev_repository = self.load_color(
            parser=parser,
            color_config=self.CONFIG_CLR_DEV_REPOSITORY,
            default=self.clr_dev_repository)

    def load_section_list(self, parser, section):
        """Load the given section containing a list from ~/.githubtrendingconfig.

        :type parser: :class:`ConfigParser.RawConfigParser`
        :param parser: An instance of `ConfigParser.RawConfigParser`.

        :type section: str
        :param section: The sectino to load.

        :rtype: dict
        :return: Collection of repositries stored in config.
        :raises: 'Exception` if an error occurred reading from the parser.
        """
        repositories = parser.get(self.CONFIG_SECTION, section)
        repositories = repositories.strip()
        return ast.literal_eval(repositories)

    def save_cache(self):
        """Save the current set of repositorys and cache to ~/.githubtrending."""
        if self.repositories is not None and \
                len(self.repositories) > self.MAX_ITEM_CACHE_SIZE:
            self.repositories= self.repositories[-self.MAX_ITEM_CACHE_SIZE//2:]
        config_file_path = self.get_config_path(self.CONFIG)
        parser = configparser.RawConfigParser()
        parser.add_section(self.CONFIG_SECTION)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_GENERAL,
                   self.clr_general)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_TOOLTIP,
                   self.clr_tooltip)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_ERROR,
                   self.clr_error)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_VIEW_INDEX,
                   self.clr_view_index)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_USER,
                   self.clr_user)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_REP_REPOSITORY,
                   self.clr_rep_repository)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_DESCRIPTION,
                   self.clr_description)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_PROGRAMMING_LANGUAGE,
                   self.clr_programming_language)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_TOTAL_STARS,
                   self.clr_total_stars)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_FORKS,
                   self.clr_forks)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_STARS_TRENDING,
                   self.clr_stars_trending)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_OWNER,
                   self.clr_owner)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_ORGANIZATION,
                   self.clr_organization)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_CLR_DEV_REPOSITORY,
                   self.clr_dev_repository)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_SHOW_TIP,
                   self.show_tip)
        parser.set(self.CONFIG_SECTION,
                   self.CONFIG_REPOSITORIES,
                   self.repositories)
        with open(config_file_path, 'w+') as config_file:
            parser.write(config_file)
