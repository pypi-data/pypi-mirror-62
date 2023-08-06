import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mywordcount_bas",
    version="0.0.1",
    author="databash",
    author_email="author@example.com",
    description="Example of package to deploy in PyPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bash-/pypi-deploy-example",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)