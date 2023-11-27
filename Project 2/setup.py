from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1.0",
    author="Anuj Kumar Shah",
    author_email="ashah5@mail.yu.edu",
    description="A package for extracting and analyzing web data",
    long_description=open(
        "README.md"
    ).read(),  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    url="https://github.com/anuzz999/DAV-5400",
    packages=find_packages(where="src"),  # Specify the directory to find packages
    package_dir={
        "": "src"
    },  # Specify the src directory as the place to look for packages
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.2.0",
        "beautifulsoup4>=4.9.3",
    ],
    classifiers=[
        # Full list: https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum version requirement of the package
)
