import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="matsim-tools",
    version="0.0.4",
    description="MATSim Agent-Based Transportation Simulation Framework - official python analysis tools",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/matsim-vsp/matsim-python-tools",
    author="VSP-Berlin",
    author_email="laudan@tu-berlin.de",
    license="GPL-3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
    ],
    packages=["matsim"],
    install_requires=['pandas'], # ,'geopandas','shapely'],
    entry_points={},
)
