from setuptools import setup, find_packages
from os import path

pkg_name = "element_deeplabcut"
here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), "r") as f:
    long_description = f.read()

with open(path.join(here, "requirements.txt")) as f:
    requirements = f.read().splitlines()

with open(path.join(here, pkg_name, "version.py")) as f:
    exec(f.read())

setup(
    name=pkg_name.replace("_", "-"),
    version=__version__,
    description="DataJoint Element for Continuous Behavior Tracking via DeepLabCut",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DataJoint",
    author_email="info@vathes.com",
    license="MIT",
    url=f'https://github.com/datajoint/{pkg_name.replace("_", "-")}',
    keywords="neuroscience behavior deeplabcut datajoint",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    scripts=[],
    install_requires=[
        "datajoint>=0.13",
        "element-interface>=0.3.0",
        "opencv-python-headless",
        "element-lab>=0.2.0",
        "element-animal>=0.1.5",
        "element-session>=0.1.2",
        "element-interface>=0.5.0",
        "ipykernel>=6.0.1",
        "pygit2",
        "graphviz",  # This worked to me installing using conda, not pip! -> pip install anaconda graphviz at the very beginning
    ],
    extras_requires={
        "default": ["deeplabcut[tf]>=2.2.1.1"],
        "apple_mchips": [
            "'deeplabcut[apple_mchips]'",
            "tables=3.7.0",
            "tensorflow-deps",
            # "--upgrade tensorflow_macos==2.10.0", ##issue with keras.legacy after installing keras -c apple
            # conda install keras -c apple
        ],
    },
)

# TO-DO: CHECK THIS FILE TO INSTALL ELEMENT IN ANOTHER CONDA ENVIRONMENT
"""
!!!! For M2 downgrade tensorflow-macos and keras to 2.12.0
tensorboard                   2.12.3
tensorboard-data-server       0.7.1
tensorboard-plugin-wit        1.8.1
tensorflow                    2.13.0
tensorflow-estimator          2.12.0
tensorflow-macos              2.12.0
tensorflow-metal              1.0.1
tensorpack                    0.11
keras                         2.12.0
"""
