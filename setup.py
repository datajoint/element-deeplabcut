from setuptools import setup, find_packages
from os import path

pkg_name = "element_deeplabcut"
here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), "r") as f:
    long_description = f.read()

with open(path.join(here, pkg_name, "version.py")) as f:
    exec(f.read())

setup(
    name=pkg_name.replace("_", "-"),
    version=__version__,
    description="DataJoint Element for Continuous Behavior Tracking via DeepLabCut",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DataJoint",
    author_email="info@datajoint.com",
    license="MIT",
    url=f'https://github.com/datajoint/{pkg_name.replace("_", "-")}',
    keywords="neuroscience behavior deeplabcut pose-estimation science datajoint",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    scripts=[],
    install_requires=[
        "datajoint>=0.14.0",
        "graphviz",
        "pydot",
        "ipykernel",
        "ipywidgets",
    ],
    extras_require={
        "dlc_default": [
            "deeplabcut[tf] @ git+https://github.com/DeepLabCut/DeepLabCut.git@pytorch_dlc"
        ],
        "dlc_apple_mchips": [
            "tensorflow-macos==2.12.0",
            "tensorflow-metal",
            "tables==3.7.0",
            "deeplabcut",
        ],
        "dlc_gui": [
            "deeplabcut[gui] @ git+https://github.com/DeepLabCut/DeepLabCut.git@pytorch_dlc"
        ],
        "elements": [
            "element-lab @ git+https://github.com/datajoint/element-lab.git",
            "element-animal @ git+https://github.com/datajoint/element-animal.git",
            "element-session @ git+https://github.com/datajoint/element-session.git",
            "element-interface @ git+https://github.com/datajoint/element-interface.git",
        ],
        "tests": ["pytest", "pytest-cov", "shutils"],
    },
)
