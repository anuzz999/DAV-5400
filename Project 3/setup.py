from setuptools import setup, find_packages

setup(
    name="spy_edas",
    version="0.1.0",
    author="Anuj Kumar Shah",
    author_email="ashah5@mail.yu.edu",
    description="A package for performing inference analysis on options data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anuzz999/DAV-5400/tree/main/Project%203",  # Replace with your repo URL
    packages=find_packages(where="src"),  # Adjust if your structure is different
    package_dir={"": "src"},  # Adjust according to your package structure
    install_requires=[
        "pandas>=1.2.0",
        "numpy>=1.19.2",
        "matplotlib>=3.3.2",
        "seaborn>=0.11.0",
        "scikit-learn>=0.24.1",  # Add other dependencies as needed
    ],
    classifiers=[
        # Full list: https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Change the license if different
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Adjust based on your compatibility requirements
)
