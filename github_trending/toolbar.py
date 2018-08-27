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
from pygments.token import Token


class Toolbar(object):
    """Show information about the aws-shell in a tool bar.

    :type handler: callable
    :param handler: Wraps the callable `get_toolbar_items`.
    """

    def __init__(self):
        self.handler = self._create_toolbar_handler()

    def _create_toolbar_handler(self):
        """Create the toolbar handler.

        :rtype: callable
        :return: get_toolbar_items.
        """

        def get_toolbar_items(_):
            """Return the toolbar items.

            :type _: :class:`prompt_toolkit.Cli`
            :param _: (Unused)

            :rtype: list
            :return: A list of (pygments.Token.Toolbar, str).
            """
            return [
                (Token.Toolbar, ' [F10] Exit ')
            ]

        return get_toolbar_items
