import re
from setuptools import setup

with open("account/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

setup(
    version=version,
    install_requires=["Django>=2.0.0"],
    tests_require=[],
    test_suite="runtests.runtests",
)
