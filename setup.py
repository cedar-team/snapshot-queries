import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snapshot-queries",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    license="MIT",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "sqlparse>=0.4.1",
        "attrs>=20.3.0",
        "pygments>=2.8.1"
    ],
    extras_require={
        'test': [
            "django>=2.2",
            "sqlalchemy>=1",
            "snapshottest==0.5.1",
            "psycopg2-binary==2.8.6"
        ]
    },
)
