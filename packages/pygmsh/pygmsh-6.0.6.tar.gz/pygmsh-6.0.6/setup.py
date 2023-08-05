import os

from setuptools import find_packages, setup

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "pygmsh", "__about__.py"), "rb") as f:
    exec(f.read(), about)


setup(
    name="pygmsh",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    packages=find_packages(),
    description="Python frontend for Gmsh",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=about["__website__"],
    project_urls={
        "Code": "https://github.com/nschloe/meshio",
        "Documentation": "https://pygmsh.readthedocs.org/en/latest",
        "Issue tracker": "https://github.com/nschloe/meshio/issues",
    },
    license=about["__license__"],
    platforms="any",
    install_requires=["meshio >=4.0, <5.0", "numpy >= 1.9"],
    python_requires=">=3.6",
    keywords=["mesh", "gmsh", "mesh generation", "mathematics"],
    classifiers=[
        about["__status__"],
        about["__license__"],
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
