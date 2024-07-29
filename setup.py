import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def read_file(fname) -> str:
    with open(fname, encoding='utf-8') as f:
        return f.read()


setuptools.setup(
    name="python-artifiacts-mmo-client", # Replace with your own username
    version="1",
    author="chomes",
    author_email="jaayjay@gmail.com",
    description="Python API client to manage the characters and mobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chomes/python-artifiacts-mmo-client",
    packages=[
        "requests==2.32.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)