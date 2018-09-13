![Imgur](https://i.imgur.com/dwxZr8T.gif)

[![PyPI](https://img.shields.io/pypi/pyversions/github-trending-cli.svg)](https://pypi.python.org/pypi/github-trending-cli/) [![License](http://img.shields.io/:license-apache-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

github-trending
================

`github-trending` brings Github Trending to the terminal, allowing you to **view** the following without leaving your command line:

* Github Trending
* Repository README

Combine `github-trending` with pipes, redirects, and other command line utilities.  Output to pagers, write to files, automate with cron, etc.

`github-trending` comes with a handy **optional auto-completer with interactive help**:

![Imgur](https://i.imgur.com/fwHg07X.png)

## Index

### General

* [Syntax](#syntax)
* [Auto-Completer and Interactive Help](#auto-completer-and-interactive-help)
* [Customizable Highlighting](#customizable-highlighting)
* [Commands](#commands)

### Features

* [View Trending](#view-trending)
* [View Repository README](#view-repository-readme)
* [Combine With Pipes and Redirects](#combine-with-pipes-and-redirects)
* [View Results in a Browser](#view-in-a-browser)

### Installation

* [Installation](#installation)
    * [Pip Installation](#pip-installation)
    * [Virtual Environment Installation](#virtual-environment-installation)
    * [Supported Python Versions](#supported-python-versions)
    * [Supported Platforms](#supported-platforms)
* [Developer Installation](#developer-installation)

### Misc

* [Contributing](#contributing)
* [Credits](#credits)
* [Contact Info](#contact-info)
* [License](#license)

## Syntax

Usage:

    $ gt <command> [params] [options]

## Auto-Completer and Interactive Help

Optionally, you can enable fish-style completions and an auto-completion menu with interactive help:

    $ github-trending

Within the auto-completer, the same syntax applies:

    github> gt <command> [params] [options]

![Imgur](https://i.imgur.com/fwHg07X.png)

## Customizable Highlighting

You can control the ansi colors used for highlighting by updating your `~/.githubtrendingconfig` file.

Color options include:

```
'black', 'red', 'green', 'yellow',
'blue', 'magenta', 'cyan', 'white'
```

For no color, set the value(s) to `None`.

## Commands

![Imgur](https://i.imgur.com/eer1XsJ.png)

## View Trending

View the Github Trending.

Usage:

    $ gt trend [option] [limit]

Examples:

    $ gt trend
    $ gt trend --language python
    $ gt trend --dev
    $ gt trend --monthly
    $ gt trend --limit 10

![Imgur](https://i.imgur.com/5Bxmdld.png)

## View Repository README

View the Repository README

Usage:

    $ gt view [user/repository]

![Imgur](https://i.imgur.com/Liq7Wvq.png)
![Imgur](https://i.imgur.com/VYLklBq.png)

## Combine With Pipes and Redirects

Output to pagers, write to files, automate with cron, etc.

Examples:

    $ gt trend -la Python -d | less
    $ gt view blue-9/github-trending > README.md

![Imgur](https://i.imgur.com/tKjJwEU.png)

## View in a Browser

View the linked web content in your default browser instead of your terminal.

Usage:

    $ gt <command> [params] [options] -b
    $ gt <command> [params] [options] --browser

## Installation

### Pip Intallation

[![PyPI version](https://badge.fury.io/py/github-trending-cli.svg)](http://badge.fury.io/py/github-trending-cli) [![PyPI](https://img.shields.io/pypi/pyversions/github-trending-cli.svg)](https://pypi.python.org/pypi/github-trending-cli/)

`github-trending` is hosted on [PyPI](https://pypi.python.org/pypi/github-trending-cli).  The following command will install `github-trending`:

    $ pip install github-trending-cli

You can also install the latest `github-trending` from GitHub source which can contain changes not yet pushed to PyPI:

    $ pip install git+https://github.com/blue-9/github-trending.git

If you are not installing in a virtualenv, run with `sudo`:

    $ sudo pip install github-trending-cli

Once installed, run the optional `github-trending` auto-completer with interactive help:

    $ github-trending

Run commands:

    $ gt <command> [param] [optional]

### Mac OS X 10.11 El Capitan Users

There is a known issue with Apple and its included python package dependencies (more info at https://github.com/pypa/pip/issues/3165). We are investigating ways to fix this issue but in the meantime, to install github-trending, you can run:

    $ sudo pip install github-trending --upgrade --ignore-installed six

### Supported Python Versions

* Python 2.6
* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5

### Supported Platforms

* Mac OS X
    * Tested on OS X 10.12

## Developer Installation

If you're interested in contributing to `github-trending-cli`, run the following commands:

    $ git clone https://github.com/blue-9/github-trending.git
    $ pip install -e .
    $ github-trending
    $ gt <command> [params] [options]

## Contributing

Contributions are welcome!

Review the [Contributing Guidelines](https://github.com/blue-9/github-trending/blob/master/CONTRIBUTING.md) for details on how to:

* Submit issues
* Submit pull requests

## Credits

* [haxor-news](https://github.com/donnemartin/haxor-news) by [donnemartin](https://github.com/donnemartin)
* [mdv](https://github.com/axiros/terminal_markdown_viewer) by [axiros](https://github.com/axiros)
* [github-ternding](https://github.com/evyatarmeged/github-trending) by [evyatarmeged](https://github.com/evyatarmeged)
* [click](https://github.com/pallets/click) by [mitsuhiko](https://github.com/mitsuhiko)
* [python-prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit) by [jonathanslenders](https://github.com/jonathanslenders)
* [requests](https://github.com/kennethreitz/requests) by [kennethreitz](https://github.com/kennethreitz)

## Contact Info

Feel free to contact me to discuss any issues, questions, or comments.

My contact info can be found on my [GitHub page](https://github.com/blue-9).

## License

[![License](http://img.shields.io/:license-apache-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

    Copyright 2018 Yuya Chiba

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
