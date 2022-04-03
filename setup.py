import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="malapiclient",
    version="0.1.0",
    author="Jonathan Lo",
    author_email="jonathanlo411@gmail.com",
    description="A client to utilize MyAnimeList's APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanlo411/malapiclient",
    project_urls={
        "Bug Tracker": "https://github.com/jonathanlo411/malapiclient/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "secrets",
    ]
)