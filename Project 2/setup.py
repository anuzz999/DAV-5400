from setuptools import setup, find_packages

setup(
    name="my_package",  # Replace with your package's name
    version="0.1.0",  # Replace with your package's version
    author="Anuj Kumar Shah",  # Replace with your name
    author_email="ashah5@mail.yu.edu",  # Replace with your email
    description="A package for extracting and analyzing web data",  # Provide a short description
    long_description=open(
        "README.md"
    ).read(),  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    url="https://github.com/anuzz999/DAV-5400",  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.2.0",
        "beautifulsoup4>=4.9.3",
        # Add other dependencies as needed
    ],
    classifiers=[
        # Classifiers help users find your project by categorizing it.
        # Full list: https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum version requirement of the package
)
