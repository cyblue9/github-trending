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

SUBCOMMANDS = {
    'trend': 'Trend repositories',
    'view': 'View repository README',
}
ARGS_OPTS_LOOKUP = {
    'trend': {
        'args': [],
        'opts': [
            '--language python',
            '-la python',
            '--dev',
            '-d',
            '--weekly',
            '-w',
            '--monthly',
            '-m',
            '--browser',
            '-b',
            '--limit 10',
            '-li 10',
        ],
    },
    'view': {
        'args': ['user/repository', ],
        'opts': [
            '--browser',
            '-b',
        ],
    },
}
META_LOOKUP = {
    'user/repository': 'View README of repository(ex:blue-9/github-trending) (string)',
    '--language python': 'View specific language trending (string)',
    '-la': 'View specific language trending (string)',
    '--dev': 'View developers trending (string)',
    '-d': 'View developers trending (flag)',
    '--weekly': 'View 1 week trending (flag)',
    '-w': 'View 1 week trending (flag)',
    '--monthly': 'View 1 month trending (flag)',
    '-m': 'View 1 month trending (flag)',
    '--browser': 'View in a browser instead of the terminal (flag)',
    '-b': 'View in a browser instead of the terminal (flag)',
    '--limit 10': 'Limits the number of items displayed (int)',
    '-li 10': 'Limits the number of items displayed (int)',
}
META_LOOKUP.update(SUBCOMMANDS)
