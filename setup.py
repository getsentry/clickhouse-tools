from setuptools import find_packages, setup
from typing import Sequence


def get_requirements() -> Sequence[str]:
    with open("requirements.txt") as fp:
        return [
            x.strip() for x in fp.read().split("\n") if not x.startswith(("#", "--"))
        ]


setup(
    name="sentry-clickhouse-tools",
    version=0,
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    include_package_data=True,
    install_requires=get_requirements(),
    entry_points={"console_scripts": ["sentry-clickhouse-tools=cli:main"]},
)
