from setuptools import setup, find_packages

setup(
    name="spy_analysis",
    version="0.2.0",
    author="Anuj Kumar Shah",
    author_email="ashah5@mail.yu.edu",
    description="A package for performing advanced data analysis including EDA, time series, and predictive modeling on SPY options data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anuzz999/DAV-5400/tree/main/Project%204",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.2.0",
        "numpy>=1.19.2",
        "matplotlib>=3.3.2",
        "seaborn>=0.11.0",
        "scikit-learn>=0.24.1",
        "statsmodels>=0.12.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
