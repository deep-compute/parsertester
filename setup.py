from setuptools import setup, find_packages

setup(
    name="parsertester",
    version="0.1",
    description="Helps in iteratively developing string parsing functions",
    keywords="parsertester",
    author="Prashanth Ellina",
    author_email="Use the github issues",
    url="https://github.com/deep-compute/parsertester",
    license="MIT License",
    install_requires=[],
    package_dir={"parsertester": "parsertester"},
    packages=find_packages("."),
    include_package_data=True,
    entry_points={"console_scripts": ["parsertester = parsertester:main"]},
)
