import setuptools
import pathlib

import pkg_resources
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snapshot-queries",
    version="0.0.1",
    author="Cedar",
    author_email="support@cedar.com",
    license="MIT",
    description="A tool for capturing queries executed in Django and SqlAlchemy",
    long_description=long_description,
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
    packages=setuptools.find_packages(),
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
                pathlib.Path("requirements.txt").read_text()
            )
        ]
    },
)
