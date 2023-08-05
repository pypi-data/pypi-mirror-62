import os

from setuptools import find_packages, setup

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "tuna", "__about__.py"), "rb") as f:
    exec(f.read(), about)


setup(
    name="tuna",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    packages=find_packages(),
    description="Visualize Python profiles in the browser",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nschloe/tuna",
    license=about["__license__"],
    platforms="any",
    python_requires=">=3.6",
    classifiers=[
        about["__status__"],
        about["__license__"],
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: User Interfaces",
    ],
    entry_points={"console_scripts": ["tuna = tuna.cli:main"]},
    package_data={
        "tuna": [
            "web/*.html",
            "web/static/*.js",
            "web/static/*.css",
            "web/static/favicon256.png",
        ]
    },
)
