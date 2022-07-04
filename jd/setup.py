import os
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# ref: https://stackoverflow.com/questions/26900328/install-dependencies-from-setup-py
lib_path = os.path.dirname(os.path.realpath(__file__))
requirements_path = lib_path + '/requirements.txt'

if os.path.isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name="jd",
    version="0.3.7",
    author="Hyunjong Kim",
    author_email="fibremint@gmail.com",
    description="provide tools for the prediction of the JD data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://example.com",
    project_urls={
        "Bug Tracker": "https://example.com",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=install_requires
)