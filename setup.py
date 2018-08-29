from github_trending.__init__ import __version__
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(
    description=('View Github Trending and repository README from the command line'),
    author='Yuya Chiba',
    url='https://github.com/blue-9/github-trending',
    download_url='https://pypi.python.org/pypi/github-trending-cli',
    author_email='cy.blue.9@gmail.com',
    version=__version__,
    license='Apache License 2.0',
    install_requires=[
        'click>=5.1,<7.0',
        'colorama>=0.3.3,<1.0.0',
        'requests>=2.4.3,<3.0.0',
        'pygments>=2.0.2,<3.0.0',
        'prompt-toolkit>=1.0.0,<1.1.0',
        'six>=1.9.0,<2.0.0',
    ],
    extras_require={
        'testing': [
            'mock>=1.0.1,<2.0.0',
            'tox>=1.9.2,<2.0.0'
        ],
    },
    entry_points={
        'console_scripts': [
            'github-trending = github_trending.main:cli',
            'gt = github_trending.main_cli:cli'
        ]
    },
    packages=find_packages(),
    scripts=[],
    name='github-trending-cli',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
