# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typic',
 'typic.constraints',
 'typic.ext',
 'typic.ext.schema',
 'typic.serde',
 'typic.types']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.3.1,<0.4.0', 'pendulum>=2.0,<3.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['typing-extensions>=3.7,<4.0'],
 'schema': ['fastjsonschema>=2.14,<3.0']}

setup_kwargs = {
    'name': 'typical',
    'version': '2.0.0b15',
    'description': 'Typical: Take Typing Further.',
    'long_description': 'Typical: Take Typing Further. :duck:\n=====================================\n![image](docs/_static/typical.png)\n\n[![image](https://img.shields.io/pypi/v/typical.svg)](https://pypi.org/project/typical/)\n[![image](https://img.shields.io/pypi/l/typical.svg)](https://pypi.org/project/typical/)\n[![image](https://img.shields.io/pypi/pyversions/typical.svg)](https://pypi.org/project/typical/)\n[![image](https://img.shields.io/github/languages/code-size/seandstewart/typical.svg?style=flat)](https://github.com/seandstewart/typical)\n![Test & Lint](https://github.com/seandstewart/typical/workflows/Test%20&%20Lint/badge.svg)\n[![Coverage](https://codecov.io/gh/seandstewart/typical/branch/master/graph/badge.svg)](https://codecov.io/gh/seandstewart/typical)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Netlify Status](https://api.netlify.com/api/v1/badges/982a0ced-bb7f-4391-87e8-1957071d2f66/deploy-status)](https://app.netlify.com/sites/typical-python/deploys)\n\nTake Typing Further with Typical. Make your annotations work for you.\n\n## Quickstart\nIn order to install, simply `pip3 install typical` and annotate to your\nheart\'s content! :duck:\n\nOr, if you\'re building an application, you should use\n[Poetry](poetry.eustace.io): `poetry add typical`\n\n\n## Updates\nSee the [Changelog](CHANGELOG.md).\n\n## Documentation\nSee the full documentation\n[Here](https://typical-python.seandstewart.io/).\n\n\n## Motivations\n\nIn the world of web-services development, type-safety becomes necessary\nfor the sanity of your code and your fellow developers. This is not to\nsay that static-typing is the solution - When it comes to the external\nentrypoints to your code, not even a compiler is going to help you.\n\nWith Python3, type annotations were introduced. With Python3.7, the\nlibrary was completely re-written for performance and ease-of-use. Type\nannotations are here to stay and I couldn\'t be happier about it.\n\nHowever, there is one place where annotations fall down. There is no\nprovided path for ensuring the type-safety of your methods, functions,\nand classes. This means if you\'re receiving data from an external\nsource, (such as with a web service) you still need to do this work\nyourself.\n\nUntil now.\n\n\n## Automatic, Guaranteed Duck-Typing\n\nBehold, the power of *Typical*:\n\n```python\n>>> import typic\n>>>\n>>> @typic.al\n>>> def multi(a: int, b: int):\n...    return a * b\n...\n>>> multi(\'2\', \'3\')\n6\n```\n\nTake it further...\n\n```python\n>>> import dataclasses\n>>> import enum\n>>> import typic\n>>>\n>>> class DuckType(str, enum.Enum):\n...     MAL = \'mallard\'\n...     BLK = \'black\'\n...     WHT = \'white\'\n... \n>>> @typic.al\n... @dataclasses.dataclass\n... class Duck:\n...     type: DuckType\n...     name: str\n...\n>>> donald = Duck(\'white\', \'Donald\')\n>>> donald.type\n<DuckType.WHT: \'white\'>\n```\n\nThis is all fine and dandy, but can we go... further? :thinking:\n\n```python\n>>> class DuckRegistry:\n...     """A Registry for all the ducks"""\n...     \n...     @typic.al\n...     def __init__(self, *duck: Duck):\n...         self._reg = {x.name: x for x in duck}\n... \n...     @typic.al\n...     def add(self, duck: Duck):\n...         self._reg[duck.name] = duck\n... \n...     @typic.al\n...     def find(self, name: str):\n...         """Try to find a duck by its name. Otherwise, try with type."""\n...         if name not in self._reg:\n...             matches = [x for x in self._reg.values() if x.type == name]\n...             if matches:\n...                 return matches[-1] if len(matches) == 1 else matches\n...         return self._reg[name]\n... \n>>> registry = DuckRegistry({\'type\': \'black\', \'name\': \'Daffy\'})\n>>> registry.find(\'Daffy\')\nDuck(type=<DuckType.BLK: \'black\'>, name=\'Daffy\')\n>>> registry.add({\'type\': \'white\', \'name\': \'Donald\'})\n>>> registry.find(\'Donald\')\nDuck(type=<DuckType.WHT: \'white\'>, name=\'Donald\')\n\n>>> registry.add({\'type\': \'goose\', \'name\': \'Maynard\'})\nTraceback (most recent call last):\n ...\nValueError: \'goose\' is not a valid DuckType\n```\n\n### What Just Happended Here?\n\nWhen we wrap a callable with `@typic.al`, the wrapper reads the\nsignature of the callable and automatically coerces the incoming data to\nthe type which is annotated. This includes varargs (`*args` and\n`**kwargs`). This means that you no longer need to do the work of\nconverting incoming data yourself. You just need to signal what you\nexpect the data to be with an annotation and **Typical** will do the\nrest.\n\nThe `ValueError` we see in the last operation is what we  can expect when\nattempting to supply an invalid value for the Enum class we used above.\nRather than have to write code to cast this data and handle stuff that\'s\ninvalid, you can rest easy in the guarantee that the data you expect is\nthe data you\'ll get.\n\n### What\'s Supported?\n\nAs of this version, **Typical** can parse the following inputs into\nvalid Python types and classes:\n* JSON\n* Python literals (via\n  [ast.literal_eval](https://docs.python.org/3/library/ast.html#ast.literal_eval))\n* Date-strings and Unix Timestamps (via\n  [pendulum](https://pendulum.eustace.io/))\n* Custom `NewType` declarations.\n* and so much more...\n\n### Limitations\n\n#### Forward Refs\nA "forward reference" is a reference to a type which has either not yet\nbeen defined, or is not available within the module which the annotation\nlives. This is noted by encapsulating the annotation in quotes, e.g.:\n`foo: \'str\' = \'bar\'`. Beware of using such syntax in combination with\nTypical. Typical makes use of `typing.get_type_hints`, which scans the\nnamespace(s) available to the given object to resolve annotations. If\nthe annotation is unavailable, a `NameError` will be raised. This\nbehavior is considered valid. If you wish to make use of Typical for\ntype-coercion, make sure the annotated type is in the namespace of the\nobject you\'re wrapping and avoid Forward References if at all possible.\n\n#### Special Forms\nThere is a subset of type annotations which are \'suscriptable\' -\nmeaning you can specify what other types this annotation may resolve\nto. In a few of those cases, the intended type for the incoming data\nis too ambiguous to resolve. The following annotations are special\nforms which cannot be resolved:\n* Union\n* Any\n\nBecause these signal an unclear resolution, Typical will ignore this\nflavor of annotation, leaving it to the developer to determine the\nappropriate action.\n\n\n## How to Contribute\n1.  This project is packaged and distributed with\n    [Poetry](https://poetry.eustice.io)\n2.  Check for open issues or open a fresh issue to start a discussion\n    around a feature idea or a bug.\n2.  Create a branch on Github for your issue or fork\n    [the repository](https://github.com/seandstewart/que) on GitHub to\n    start making your changes to the **master** branch.\n4.  Write a test which shows that the bug was fixed or that the\n    feature works as expected.\n5.  Send a pull request and bug the maintainer until it gets merged\n    and published. :)\n\n\nHappy Typing :duck:\n',
    'author': 'Sean Stewart',
    'author_email': 'sean_stewart@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/seandstewart/typical',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
