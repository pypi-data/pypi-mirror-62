# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tokelor']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'colorama>=0.4,<0.5']

entry_points = \
{'console_scripts': ['tokelor = tokelor.cli:main']}

setup_kwargs = {
    'name': 'tokelor',
    'version': '0.1.6',
    'description': 'Visualize Python token stream produced by tokenize module.',
    'long_description': '# tokelor\n![PyPI](https://img.shields.io/pypi/v/tokelor) \n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tokelor)\n![License](https://img.shields.io/github/license/lensvol/tokelor)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nVisualize Python token stream produced by tokenize module.\n\n## Example\n\n![Example usage](https://raw.githubusercontent.com/lensvol/tokelor/master/docs/example.png)\n\n## Usage\n```\n# tokelor --help\nUsage: tokelor [OPTIONS] SOURCE\n\n  Visualize Python token stream produced by tokenize module.\n\nOptions:\n  --nl / --no-nl      Display newline tokens.\n  --bare / --no-bare  Replace bold text with underlinings.\n  --help              Show this message and exit.\n```\n\n## Installation\n\n```shell script\n# pip install tokelor\n```\n\n## Getting started with development\n\n```shell script\n# git clone git@github.com:lensvol/tokelor.git\n# poetry install --develop\n```\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n\n## Authors\n\n* **Kirill Borisov** ([lensvol@gmail.com](mailto:lensvol@gmail.com))\n',
    'author': 'Kirill Borisov',
    'author_email': 'lensvol@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lensvol/tokelor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
