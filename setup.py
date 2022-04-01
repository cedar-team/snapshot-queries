import setuptools
import pathlib

import pkg_resources
import setuptools

__version__ = "0.1.0"

setuptools.setup(
    name="snapshot-queries",
    version="0.0.1",
    author="Cedar",
    author_email="support@cedar.com",
    license="MIT",
    description="A tool for capturing queries executed in Django and SqlAlchemy",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/cedar-team/snapshot-queries",
    project_urls={
        "Bug Tracker": "https://github.com/cedar-team/snapshot-queries",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(
        include=['snapshot_queries*'],
    ),
    python_requires=">=3.6",
    install_requires=[
        str(requirement)
        for requirement in pkg_resources.parse_requirements(
            pathlib.Path("requirements.txt").read_text()
        )
    ],
    extras_require={
        "test": [
            str(requirement)
            for requirement in pkg_resources.parse_requirements(
                pathlib.Path("test.requirements.txt").read_text()
            )
        ],
        # NOTE: Since this is extra is called "snapshottest", the "test" extra
        #       should be renamed to "development" to avoid confusion
        "snapshottest": ["snapshottest"],
    },
)
