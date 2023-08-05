# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argser']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=1.1,<2.0']

extras_require = \
{'all': ['tabulate>=0.8.5,<0.9.0', 'argcomplete>=1.10,<2.0'],
 'argcomplete': ['argcomplete>=1.10,<2.0'],
 'tabulate': ['tabulate>=0.8.5,<0.9.0']}

entry_points = \
{'console_scripts': ['argser = argser.__main__:main']}

setup_kwargs = {
    'name': 'argser',
    'version': '0.0.16',
    'description': 'Arguments parsing without boilerplate.',
    'long_description': '# argser\n\n[![PyPI version](https://badge.fury.io/py/argser.svg)](http://badge.fury.io/py/argser)\n[![Downloads](https://pepy.tech/badge/argser)](https://pepy.tech/project/argser)\n[![Build Status](https://github.com/vanyakosmos/argser/workflows/tests/badge.svg)](https://github.com/vanyakosmos/argser/actions?workflow=tests)\n[![Coverage](https://codecov.io/gh/vanyakosmos/argser/branch/master/graph/badge.svg)](https://codecov.io/gh/vanyakosmos/argser)\n[![Docs](https://readthedocs.org/projects/argser/badge/?version=stable)](https://argser.readthedocs.io/en/stable/)\n\n[GitHub](https://github.com/vanyakosmos/argser) |\n[PyPI](https://pypi.org/project/argser/) |\n[Docs](https://argser.readthedocs.io/en/stable) |\n[Examples](https://argser.readthedocs.io/en/stable/examples.html) |\n[Installation](https://argser.readthedocs.io/en/stable/installation.html) |\n[Changelog](CHANGELOG.md)\n\nArguments parsing without boilerplate.\n\n## Features:\n- arguments and type hints in IDE\n- easy nested sub-commands\n- sane defaults for arguments\' params (ie if default of arg is 3 then type should be int, or when annotation/type/default is `bool` then generate 2 arguments: for true value `--arg` and for false `--no-arg`, ...)\n- 𝕡𝕣𝕖𝕥𝕥𝕪 𝕡𝕣𝕚𝕟𝕥𝕚𝕟𝕘\n- support for argparse actions\n- common options/arguments reusability\n- auto shortcuts generation: `--verbose -> -v, --foo_bar -> --fb`\n- [auto completion](https://argser.readthedocs.io/en/latest/examples.html#auto-completion) in shell (tnx to [argcomplete](https://argcomplete.readthedocs.io/en/latest/))\n\n\n## Installation\n\n```text\npip install argser\npip install argser[tabulate]  # for fancy tables support\npip install argser[argcomplete]  # for shell auto completion\npip install argser[all]\n```\n\n\n## Notes for examples\n\nIf second parameter of `parse_args` is string (as in almost all examples) then it will be parsed,\notherwise arguments to parse will be taken from command line.\n\n\n## Simple example\n\n```python\nfrom argser import parse_args\n\nclass Args:\n    a = \'a\'\n    foo = 1\n    bar: bool\n    bar_baz = 42, "bar_baz help"\n\nargs = parse_args(Args, show=True)\n```\n\n<details>\n<summary>argparse alternative</summary>\n\n```python\nfrom argparse import ArgumentParser\n\nparser = ArgumentParser()\nparser.add_argument(\'-a\', type=str, default=\'a\', help="str, default: \'a\'")\nparser.add_argument(\'--foo\', \'-f\', dest=\'foo\', type=int, default=1, help="int, default: 1")\nparser.add_argument(\'--bar\', \'-b\', dest=\'bar\', action=\'store_true\', help="bool, default: None")\nparser.add_argument(\'--no-bar\', \'--no-b\', dest=\'bar\', action=\'store_false\')\nparser.set_defaults(bar=None)\nparser.add_argument(\'--bar-baz\', dest=\'bar_baz\', default=42, help="int, default: 42. bar_baz help")\n\nargs = parser.parse_args()\nprint(args)\n```\n</details>\n\n```text\n❯ python playground.py -a "aaa bbb" -f 100500 --no-b\n>>> Args(bar=False, a=\'aaa bbb\', foo=100500, bar_baz=42)\n```\n\n```text\n❯ python playground.py -h\nusage: playground.py [-h] [--bar] [--no-bar] [-a A] [--foo F] [--bar-baz B]\n\noptional arguments:\n    -h, --help           show this help message and exit\n    --bar, -b            bool, default: None\n    --no-bar, --no-b\n    -a A                 str, default: \'a\'\n    --foo F, -f F        int, default: 1\n    --bar-baz B, --bb B  int, default: 42. bar_baz help\n```\n\n\n## Get arguments from function\n\n```python\nimport argser\n\ndef foo(a, b: int, c=1.2):\n    return [a, b, c]\n\nassert argser.call(foo, \'1 2 -c 3.4\') == [\'1\', 2, 3.4]\n```\n\n\n## Sub-commands\n\n```python\nfrom argser import parse_args, sub_command\n\nclass Args:\n    a: bool\n    b = []\n    c = 5\n\n    class SubArgs:\n        d = 1\n        e = \'2\'\n    sub = sub_command(SubArgs, help=\'help message for sub-command\')\n\nargs = parse_args(Args, \'-a -b a b -c 10\', parser_help=\'help message for root parser\')\nassert args.a is True\nassert args.b == [\'a\', \'b\']\nassert args.c == 10\nassert args.sub is None\n\nargs = parse_args(Args, \'--no-a -c 10 sub -d 5 -e "foo bar"\')\nassert args.a is False\nassert args.sub.d == 5\nassert args.sub.e == \'foo bar\'\n```\n\n```text\n❯ python playground.py -h\nusage: playground.py [-h] [-a] [--no-a] [-b [B [B ...]]] [-c C] {sub} ...\n\npositional arguments:\n    {sub}\n\noptional arguments:\n    -h, --help      show this help message and exit\n    -a              bool, default: None\n    --no-a\n    -b [B [B ...]]  List[str], default: []\n    -c C            int, default: 5\n```\n\n```text\n❯ python playground.py sub1 -h\nusage: playground.py sub [-h] [-d D] [-e E]\n\nhelp message for sub-command\n\noptional arguments:\n    -h, --help  show this help message and exit\n    -d D        int, default: 1\n    -e E        str, default: \'2\'\n```\n\nCan be deep nested:\n```python\nfrom argser import parse_args, sub_command\n\nclass Args:\n    a = 1\n    class Sub1:\n        b = 1\n        class Sub2:\n            c = 1\n            class Sub3:\n                d = 1\n            sub3 = sub_command(Sub3)\n        sub2 = sub_command(Sub2)\n    sub1 = sub_command(Sub1)\n\nargs = parse_args(Args, \'-a 1 sub1 -b 2 sub2 -c 3 sub3 -d 4\')\n```\n\n\n### Sub-commands from functions\n\n```python\nimport argser\nsubs = argser.SubCommands()\n\n@subs.add\ndef foo():\n    return \'foo\'\n\n@subs.add(description="foo bar")  # with additional arguments for sub-parser\ndef bar(a, b=1):\n    return [a, b]\n\nassert subs.parse(\'foo\') == \'foo\'\nassert subs.parse(\'bar 1 -b 2\') == [\'1\', 2]\n```\n',
    'author': 'Bachynin Ivan',
    'author_email': 'bachynin.i@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vanyakosmos/argser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
