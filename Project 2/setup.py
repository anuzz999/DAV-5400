from setuptools import setup, find_packages

setup(
    name="fin_data_scraper",
    version="0.2.0",
    author="Anuj Kumar Shah",
    author_email="ashah5@mail.yu.edu",
    description="A package for extracting and analyzing financial web data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anuzz999/DAV-5400",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.2.0",
        "beautifulsoup4>=4.9.3",
        "selenium>=3.141.0",
        "numpy>=1.19.5",
    ],
    classifiers=[
        # Full list: https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum version requirement of the package
    entry_points={
        "console_scripts": [
            "run-scraper=fin_data_scraper.__main__:main",  # Adjust if you have a different entry point
        ],
    },
)
