import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zetaSeq",
    version="0.0.4",
    author="Zewei Song",
    author_email="songzewei@outlook.com",
    description="A final resort for sequencing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZeweiSong/zetaSeq",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)