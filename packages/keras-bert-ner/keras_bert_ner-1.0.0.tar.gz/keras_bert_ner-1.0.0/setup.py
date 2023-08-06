import setuptools

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import call

with open("README.md","r") as f:
    long_description = f.read()

class Installation(install):
    def run(self):
        call(["pip install -r requirements.txt --no-clean"], shell=True)
        install.run(self)

setuptools.setup(
    name="keras_bert_ner",
    version="1.0.0",
    author="liushaoweihua",
    author_email="liushaoweihua@126.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liushaoweihua/keras-bert-ner.git",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=["flask", "keras", "numpy", "loguru", "requests", "termcolor", "tensorflow", "keras_contrib"],
    install_requires=["flask", "keras", "numpy", "loguru", "requests", "termcolor", "tensorflow", "keras_contrib"],
    cmdclass={'install':Installation},
)
